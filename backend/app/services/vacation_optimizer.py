from datetime import datetime, timedelta
from typing import List, Dict
from ..models.holiday import Holiday
from ..models.policy import Policy
from ..models.time_budget import TimeBudget
from itertools import combinations

def optimize_vacation(user_id: int, year: int, no_single_days: bool = False, max_vacations: int = None, db) -> Dict:
    policy = db.query(Policy).filter(Policy.user_id == user_id).first()
    time_budget = db.query(TimeBudget).filter(TimeBudget.user_id == user_id).first()
    holidays = db.query(Holiday).filter(Holiday.year == year).all()

    available_days = time_budget.accrued_days - time_budget.used_days
    blackout_dates = {datetime.strptime(d, "%Y-%m-%d").date() for d in policy.blackout_dates or []}
    holiday_dates = {h.date: h for h in holidays}

    # Generate all possible periods
    all_periods = []
    for holiday in holidays:
        holiday_date = holiday.date
        for offset in range(1, 8):
            start = holiday_date - timedelta(days=offset)
            end = holiday_date - timedelta(days=1)
            all_periods.extend(generate_period(start, end, holiday_dates, blackout_dates, available_days, no_single_days))

            start = holiday_date + timedelta(days=1)
            end = holiday_date + timedelta(days=offset)
            all_periods.extend(generate_period(start, end, holiday_dates, blackout_dates, available_days, no_single_days))

            start = holiday_date - timedelta(days=offset // 2)
            end = holiday_date + timedelta(days=offset // 2)
            all_periods.extend(generate_period(start, end, holiday_dates, blackout_dates, available_days, no_single_days))

    # Score periods
    for p in all_periods:
        p["efficiency"] = p["total_days_off"] / p["days_used"]

    # Filter and sort by efficiency
    all_periods.sort(key=lambda x: x["efficiency"], reverse=True)

    # Find combinations for max_vacations
    schedule = []
    used_days_total = 0
    used_dates = set()

    if max_vacations is not None:
        for r in range(1, min(max_vacations + 1, len(all_periods) + 1)):
            for combo in combinations(all_periods, r):
                total_used = sum(p["days_used"] for p in combo)
                if total_used == available_days:
                    temp_dates = set()
                    overlaps = False
                    for p in combo:
                        start = datetime.strptime(p["start"], "%Y-%m-%d").date()
                        end = datetime.strptime(p["end"], "%Y-%m-%d").date()
                        current = start
                        while current <= end:
                            if current in temp_dates:
                                overlaps = True
                                break
                            temp_dates.add(current)
                            current += timedelta(days=1)
                        if overlaps:
                            break
                    if not overlaps:
                        schedule = list(combo)
                        used_days_total = total_used
                        used_dates = temp_dates
                        break
            if schedule:
                break

        if not schedule:
            for period in all_periods:
                if len(schedule) >= max_vacations or used_days_total >= available_days:
                    break
                period_start = datetime.strptime(period["start"], "%Y-%m-%d").date()
                period_end = datetime.strptime(period["end"], "%Y-%m-%d").date()
                current = period_start
                overlaps = False
                while current <= period_end:
                    if current in used_dates:
                        overlaps = True
                        break
                    current += timedelta(days=1)
                if not overlaps:
                    schedule.append(period)
                    used_days_total += period["days_used"]
                    current = period_start
                    while current <= period_end:
                        used_dates.add(current)
                        current += timedelta(days=1)
            if used_days_total < available_days and schedule:
                last_period = schedule[-1]
                remaining_days = available_days - used_days_total + last_period["days_used"]
                new_end = datetime.strptime(last_period["start"], "%Y-%m-%d").date() + timedelta(days=remaining_days - 1)
                if (new_end - datetime.strptime(last_period["start"], "%Y-%m-%d").date()).days + 1 <= 14:
                    schedule[-1] = generate_period(
                        datetime.strptime(last_period["start"], "%Y-%m-%d").date(),
                        new_end,
                        holiday_dates,
                        blackout_dates,
                        available_days,
                        no_single_days
                    )[0]
                    used_days_total = available_days

    # Merge consecutive periods
    merged_schedule = []
    if schedule:
        schedule.sort(key=lambda x: datetime.strptime(x["start"], "%Y-%m-%d"))
        current = schedule[0]
        for next_period in schedule[1:]:
            current_end = datetime.strptime(current["end"], "%Y-%m-%d").date()
            next_start = datetime.strptime(next_period["start"], "%Y-%m-%d").date()
            if current_end + timedelta(days=1) >= next_start:
                current["end"] = max(current["end"], next_period["end"])
                current = regenerate_period(current, holiday_dates, blackout_dates)
            else:
                merged_schedule.append(current)
                current = next_period
        merged_schedule.append(current)

    unused_days = available_days - sum(p["days_used"] for p in merged_schedule)
    warning = f"Warning: {unused_days} days unused due to constraints" if unused_days > 0 else None

    return {"schedule": merged_schedule, "warning": warning}

def generate_period(start, end, holiday_dates, blackout_dates, available_days, no_single_days):
    periods = []
    current = start
    days_used = 0
    workdays = 0
    holidays = 0
    weekends = 0
    days = []
    explanation_parts = []

    while current <= end:
        days.append(current)
        if current.weekday() >= 5:
            pass
        elif current in holiday_dates:
            holidays += 1
            explanation_parts.append(f"{current.strftime('%a %b %-d')} {holiday_dates[current].name}")
        elif current in blackout_dates:
            return []
        else:
            days_used += 1
            workdays += 1
            explanation_parts.append(f"{current.strftime('%a %b %-d')} workday")
        current += timedelta(days=1)

    i = 0
    while i < len(days) - 1:
        if (days[i].weekday() == 5 and days[i + 1].weekday() == 6):
            weekends += 1
            explanation_parts.append(f"{days[i].strftime('%a %b %-d')}-{days[i+1].strftime('%a %b %-d')} weekend")
            i += 2
        else:
            i += 1

    total_days_off = (end - start).days + 1
    if (days_used <= available_days and 
        days_used > 0 and 
        (not no_single_days or days_used >= 2) and 
        total_days_off <= 14):
        explanation = ", ".join(explanation_parts)
        periods.append({
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d") if start != end else start.strftime("%Y-%m-%d"),
            "days_used": days_used,
            "total_days_off": total_days_off,
            "breakdown": {
                "workdays": workdays,
                "holidays": holidays,
                "weekends": weekends
            },
            "explanation": explanation
        })
    return periods

def regenerate_period(period, holiday_dates, blackout_dates):
    start = datetime.strptime(period["start"], "%Y-%m-%d").date()
    end = datetime.strptime(period["end"], "%Y-%m-%d").date()
    return generate_period(start, end, holiday_dates, blackout_dates, float('inf'), False)[0]  # No constraints for merging
