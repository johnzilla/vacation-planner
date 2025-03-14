# Architecture

## Overview
A web and mobile app to optimize vacation schedules using holidays, policies, and time budgets.

## Components
- **Frontend**: Svelte (web) + Svelte with Capacitor (mobile).
- **Backend**: FastAPI, PostgreSQL.
- **Optimizer**: Rule-based algorithm in `services/vacation_optimizer.py`.

## Flow
1. User inputs time budget (`time-budget/` page).
2. User adds employer holidays (`holidays/` page).
3. Backend optimizes schedule (`GET /suggestions`).
4. Results displayed (`suggestions/` page).

## Diagram
[User] --> [Web/Mobile Frontend] --> [API Gateway (FastAPI)] --> [PostgreSQL]
                                   --> [Optimizer]
                                   
