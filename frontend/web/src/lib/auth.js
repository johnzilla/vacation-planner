// frontend/web/src/lib/auth.js
// Authentication utilities for the Vacation Planner app

import { writable } from 'svelte/store';

// Base URL for API requests
const API_BASE_URL = 'http://localhost:8000/api';

// Create stores for authentication state
export const isAuthenticated = writable(false);
export const user = writable(null);
export const authError = writable(null);

// Initialize auth state from localStorage on app load
export function initAuth() {
  const token = localStorage.getItem('token');
  const userData = localStorage.getItem('user');

  if (token && userData) {
    isAuthenticated.set(true);
    user.set(JSON.parse(userData));
  }
}

// Register a new user
export async function register(email, password) {
  try {
    authError.set(null);
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Registration failed');
    }

    // Registration successful, now login
    return login(email, password);
  } catch (error) {
    authError.set(error.message);
    return { success: false, error: error.message };
  }
}

// Login user
export async function login(email, password) {
  try {
    authError.set(null);

    // Create form data for token endpoint
    const formData = new FormData();
    formData.append('username', email); // FastAPI OAuth expects 'username'
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/token`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();

    // Store token and user data
    localStorage.setItem('token', data.access_token);
    localStorage.setItem(
      'user',
      JSON.stringify({
        id: data.user_id,
        email: data.email,
      })
    );

    // Update stores
    isAuthenticated.set(true);
    user.set({
      id: data.user_id,
      email: data.email,
    });

    return { success: true };
  } catch (error) {
    authError.set(error.message);
    return { success: false, error: error.message };
  }
}

// Logout user
export function logout() {
  // Clear localStorage
  localStorage.removeItem('token');
  localStorage.removeItem('user');

  // Update stores
  isAuthenticated.set(false);
  user.set(null);
}

// Get auth header for authenticated requests
export function getAuthHeader() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Check if user is authenticated
export function checkAuth() {
  const token = localStorage.getItem('token');
  return !!token;
}

// Get current user
export function getCurrentUser() {
  const userData = localStorage.getItem('user');
  return userData ? JSON.parse(userData) : null;
}

// Fetch user profile
export async function getUserProfile() {
  try {
    const token = localStorage.getItem('token');
    if (!token) throw new Error('Not authenticated');

    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid
        logout();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error('Failed to fetch user profile');
    }

    return response.json();
  } catch (error) {
    authError.set(error.message);
    return null;
  }
}
