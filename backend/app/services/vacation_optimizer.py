from datetime import datetime, timedelta
from typing import List, Dict
from ..models.holiday import Holiday
from ..models.policy import Policy
from ..models.time_budget import TimeBudget
from itertools import combinations

def optimize_vacation(user_id: int, year: int, db, no_single_days: bool = False, max_vacations: int = None) -> Dict:
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
                    # Check if periods overlap
                    all_dates = set()
                    for p in combo:
                        p_dates = set(p["dates"])
                        if any(d in all_dates for d in p_dates):
                            # Periods overlap, skip
                            continue
                        all_dates.update(p_dates)
                    
                    # Calculate total days off
                    total_days_off = sum(p["total_days_off"] for p in combo)
                    
                    # If better than current best, update
                    if not schedule or total_days_off > sum(p["total_days_off"] for p in schedule):
                        schedule = combo
                        used_days_total = total_used
                        used_dates = all_dates
                        break
    else:
        # Greedy approach for no max_vacations
        remaining_days = available_days
        for period in all_periods:
            if period["days_used"] <= remaining_days:
                # Check if period overlaps with used dates
                p_dates = set(period["dates"])
                if any(d in used_dates for d in p_dates):
                    continue
                
                schedule.append(period)
                remaining_days -= period["days_used"]
                used_days_total += period["days_used"]
                used_dates.update(p_dates)
                
                if remaining_days == 0:
                    break

    # Format the result
    result = {
        "schedule": [
            {
                "start": p["start_date"].strftime("%Y-%m-%d"),
                "end": p["end_date"].strftime("%Y-%m-%d"),
                "days_used": p["days_used"],
                "total_days_off": p["total_days_off"],
                "efficiency": p["efficiency"],
                "breakdown": {
                    "workdays": p["workdays"],
                    "weekends": p["weekends"],
                    "holidays": p["holidays"]
                },
                "explanation": p["explanation"]
            }
            for p in schedule
        ],
        "warning": None
    }
    
    if not schedule:
        result["warning"] = "No optimal schedule found. Try adjusting your time budget or constraints."
    
    return result

def generate_period(start_date, end_date, holiday_dates, blackout_dates, available_days, no_single_days):
    periods = []
    
    # Skip if dates are in the past
    today = datetime.now().date()
    if end_date < today:
        return periods
    
    # Skip if start date is after end date
    if start_date > end_date:
        return periods
    
    # Skip if period is too short and no_single_days is True
    if no_single_days and (end_date - start_date).days < 1:
        return periods
    
    # Calculate workdays, holidays, and weekends
    workdays = 0
    holidays_count = 0
    weekends = 0
    dates = []
    
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        
        # Skip blackout dates
        if current_date in blackout_dates:
            current_date += timedelta(days=1)
            continue
        
        # Check if weekend
        if current_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            weekends += 1
        # Check if holiday
        elif current_date in holiday_dates:
            holidays_count += 1
        # Otherwise it's a workday
        else:
            workdays += 1
        
        current_date += timedelta(days=1)
    
    # Skip if no workdays (nothing to take off)
    if workdays == 0:
        return periods
    
    # Skip if more workdays than available days
    if workdays > available_days:
        return periods
    
    # Calculate total days off (workdays + holidays + weekends)
    total_days_off = workdays + holidays_count + weekends
    
    # Create period object
    period = {
        "start_date": start_date,
        "end_date": end_date,
        "days_used": workdays,
        "total_days_off": total_days_off,
        "workdays": workdays,
        "holidays": holidays_count,
        "weekends": weekends,
        "dates": dates,
        "explanation": f"Take {workdays} days off to get {total_days_off} days away (includes {weekends} weekend days and {holidays_count} holidays)"
    }
    
    periods.append(period)
    return periods

def regenerate_period(period, holiday_dates, blackout_dates):
    start = datetime.strptime(period["start"], "%Y-%m-%d").date()
    end = datetime.strptime(period["end"], "%Y-%m-%d").date()
    return generate_period(start, end, holiday_dates, blackout_dates, float('inf'), False)[0]  # No constraints for merging
