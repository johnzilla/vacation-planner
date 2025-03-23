# Product Context

This file provides a high-level overview of the project and the expected product that will be created. Initially it is based upon projectBrief.md (if provided) and all other available project-related information in the working directory. This file is intended to be updated as the project evolves, and should be used to inform all other modes of the project's goals and context.
2025-03-22 19:52:00 - Log of updates made will be appended as footnotes to the end of this file.

## Project Goal

* Vacation Planner is a cross-platform application designed to optimize employee vacation schedules based on holidays, employer policies, and accrued time budgets.
* The goal is to provide an easy-to-use tool that helps users maximize their time off by strategically planning vacations around holidays and weekends.

## Key Features

* Holiday Integration: Pre-compiled US federal and employer-specific holidays for 2025
* Time Budget: Users input accrued and used vacation days
* Vacation Policy: Supports blackout dates and max days (configurable)
* AI Optimization: Suggests schedules maximizing contiguous days off
* Cross-Platform: Web (SvelteKit) and mobile (Svelte + Capacitor)
* Database: SQLite for development, PostgreSQL for production
* Authentication: User authentication and saved vacation plans

## Overall Architecture

* Backend: FastAPI (Python), SQLite/PostgreSQL, SQLAlchemy
* Frontend: SvelteKit (web), Svelte + Capacitor (mobile)
* Deployment: Vercel (web), Capacitor (mobile), Fly.io (backend), Docker (full stack)
* Flow: User inputs time budget → Backend stores data → Backend optimizes schedule → Results displayed → User can save plans

## Current Status

* Early development stage (MVP)
* Solo developer project
* Basic functionality implemented
* Missing several software development resources (testing, CI/CD, etc.)
