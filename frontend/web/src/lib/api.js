// frontend/web/src/lib/api.js
// Utility functions for making API requests to the Vacation Planner backend.

// Base URL for API requests (update for production)
const API_BASE_URL = 'http://localhost:8000/api'; // Default for local dev

// Fetch vacation suggestions
export async function getSuggestions(userId, noSingleDays, maxVacations) {
  const params = new URLSearchParams({
    user_id: userId,
    no_single_days: noSingleDays,
    ...(maxVacations && { max_vacations: maxVacations })
  });
  const response = await fetch(`${API_BASE_URL}/suggestions?${params}`);
  if (!response.ok) throw new Error('Failed to fetch suggestions');
  return response.json();
}

// Fetch current time budget
export async function getTimeBudget(userId) {
  const response = await fetch(`${API_BASE_URL}/time-budget?user_id=${userId}`);
  if (!response.ok) throw new Error('Failed to fetch time budget');
  return response.json();
}

// Update time budget
export async function updateTimeBudget(userId, accruedDays, usedDays) {
  const response = await fetch(`${API_BASE_URL}/time-budget`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ accrued_days: accruedDays, used_days: usedDays })
  });
  if (!response.ok) throw new Error('Failed to update time budget');
  return response.json();
}

// Fetch employers
export async function getEmployers() {
  const response = await fetch(`${API_BASE_URL}/employers`);
  if (!response.ok) throw new Error('Failed to fetch employers');
  return response.json();
}

// Add a new holiday
export async function addHoliday(holiday) {
  const response = await fetch(`${API_BASE_URL}/holidays`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(holiday)
  });
  if (!response.ok) throw new Error('Failed to add holiday');
  return response.json();
}

// Notes:
// - Update API_BASE_URL to your production backend URL (e.g., https://your-backend.fly.dev/api).
// - Add error handling or retries as needed.
// - Extend with additional API endpoints if the backend expands.// frontend/web/src/lib/api.js
// Utility functions for making API requests to the Vacation Planner backend.

// Base URL for API requests (update for production)
const API_BASE_URL = 'http://localhost:8000/api'; // Default for local dev

// Fetch vacation suggestions
export async function getSuggestions(userId, noSingleDays, maxVacations) {
  const params = new URLSearchParams({
    user_id: userId,
    no_single_days: noSingleDays,
    ...(maxVacations && { max_vacations: maxVacations })
  });
  const response = await fetch(`${API_BASE_URL}/suggestions?${params}`);
  if (!response.ok) throw new Error('Failed to fetch suggestions');
  return response.json();
}

// Fetch current time budget
export async function getTimeBudget(userId) {
  const response = await fetch(`${API_BASE_URL}/time-budget?user_id=${userId}`);
  if (!response.ok) throw new Error('Failed to fetch time budget');
  return response.json();
}

// Update time budget
export async function updateTimeBudget(userId, accruedDays, usedDays) {
  const response = await fetch(`${API_BASE_URL}/time-budget`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ accrued_days: accruedDays, used_days: usedDays })
  });
  if (!response.ok) throw new Error('Failed to update time budget');
  return response.json();
}

// Fetch employers
export async function getEmployers() {
  const response = await fetch(`${API_BASE_URL}/employers`);
  if (!response.ok) throw new Error('Failed to fetch employers');
  return response.json();
}

// Add a new holiday
export async function addHoliday(holiday) {
  const response = await fetch(`${API_BASE_URL}/holidays`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(holiday)
  });
  if (!response.ok) throw new Error('Failed to add holiday');
  return response.json();
}

// Notes:
// - Update API_BASE_URL to your production backend URL (e.g., https://your-backend.fly.dev/api).
// - Add error handling or retries as needed.
// - Extend with additional API endpoints if the backend expands.
