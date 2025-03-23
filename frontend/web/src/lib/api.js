// frontend/web/src/lib/api.js
// Utility functions for making API requests to the Vacation Planner backend.
import { getAuthHeader } from './auth';

// Base URL for API requests (update for production)
const API_BASE_URL = '/api'; // Use relative path for proxying through Vite

// Fetch vacation suggestions
export async function getSuggestions(userId, noSingleDays, maxVacations) {
  const params = new URLSearchParams({
    user_id: userId,
    no_single_days: noSingleDays,
    ...(maxVacations && { max_vacations: maxVacations }),
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
    body: JSON.stringify({ user_id: userId, accrued_days: accruedDays, used_days: usedDays }),
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

// Add a holiday
export async function addHoliday(holiday) {
  const response = await fetch(`${API_BASE_URL}/holidays`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(holiday),
  });
  if (!response.ok) throw new Error('Failed to add holiday');
  return response.json();
}

// Saved Plans API Functions

// Get user's saved plans (requires authentication)
export async function getSavedPlans() {
  const headers = {
    ...getAuthHeader(),
    'Content-Type': 'application/json',
  };

  const response = await fetch(`${API_BASE_URL}/saved-plans`, {
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error('Authentication required');
    throw new Error('Failed to fetch saved plans');
  }

  return response.json();
}

// Get a specific saved plan (may be public or private)
export async function getSavedPlan(planId) {
  const headers = {
    ...getAuthHeader(),
    'Content-Type': 'application/json',
  };

  const response = await fetch(`${API_BASE_URL}/saved-plans/${planId}`, {
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error('Authentication required');
    if (response.status === 403) throw new Error('Not authorized to view this plan');
    if (response.status === 404) throw new Error('Plan not found');
    throw new Error('Failed to fetch saved plan');
  }

  return response.json();
}

// Create a new saved plan (requires authentication)
export async function createSavedPlan(plan) {
  const headers = {
    ...getAuthHeader(),
    'Content-Type': 'application/json',
  };

  const response = await fetch(`${API_BASE_URL}/saved-plans`, {
    method: 'POST',
    headers,
    body: JSON.stringify(plan),
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error('Authentication required');
    throw new Error('Failed to create saved plan');
  }

  return response.json();
}

// Update a saved plan (requires authentication)
export async function updateSavedPlan(planId, plan) {
  const headers = {
    ...getAuthHeader(),
    'Content-Type': 'application/json',
  };

  const response = await fetch(`${API_BASE_URL}/saved-plans/${planId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(plan),
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error('Authentication required');
    if (response.status === 403) throw new Error('Not authorized to update this plan');
    if (response.status === 404) throw new Error('Plan not found');
    throw new Error('Failed to update saved plan');
  }

  return response.json();
}

// Delete a saved plan (requires authentication)
export async function deleteSavedPlan(planId) {
  const headers = {
    ...getAuthHeader(),
  };

  const response = await fetch(`${API_BASE_URL}/saved-plans/${planId}`, {
    method: 'DELETE',
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error('Authentication required');
    if (response.status === 403) throw new Error('Not authorized to delete this plan');
    if (response.status === 404) throw new Error('Plan not found');
    throw new Error('Failed to delete saved plan');
  }

  return true;
}

// Create a share link for a saved plan (requires authentication)
export async function createShareLink(planId) {
  const headers = {
    ...getAuthHeader(),
    'Content-Type': 'application/json',
  };

  const response = await fetch(`${API_BASE_URL}/saved-plans/${planId}/share`, {
    method: 'POST',
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error('Authentication required');
    if (response.status === 403) throw new Error('Not authorized to share this plan');
    if (response.status === 404) throw new Error('Plan not found');
    throw new Error('Failed to create share link');
  }

  return response.json();
}

// Get a shared plan by token (public, no authentication required)
export async function getSharedPlan(shareToken) {
  const response = await fetch(`${API_BASE_URL}/saved-plans/shared/${shareToken}`);

  if (!response.ok) {
    if (response.status === 404) throw new Error('Shared plan not found');
    throw new Error('Failed to fetch shared plan');
  }

  return response.json();
}
