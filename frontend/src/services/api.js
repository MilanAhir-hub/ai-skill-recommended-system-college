/**
 * services/api.js
 * ----------------
 * Centralized API service for communicating with the Flask backend.
 * Uses the native Fetch API and reads the base URL from Vite environment variables.
 */

// Centralized API Base URL (configured via .env or Vite proxy fallback)
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');

/**
 * Helper to handle fetch responses and error extraction.
 */
async function handleResponse(response) {
  let data;
  try {
    data = await response.json();
  } catch (err) {
    throw new Error(`Server returned status ${response.status} with non-JSON response.`);
  }

  if (!response.ok) {
    const errorMessage = data?.message || `Request failed with status ${response.status}`;
    throw new Error(errorMessage);
  }

  return data;
}

/**
 * 1. Check API health & status
 * GET /
 */
export async function checkApiHealth() {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/` : '/';
    const response = await fetch(url);
    return await handleResponse(response);
  } catch (error) {
    throw new Error(
      error.message || 'Unable to connect to backend server. Please verify Flask is running.'
    );
  }
}

/**
 * 2. Fetch available careers catalog and their required skills
 * GET /api/careers
 */
export async function fetchCareersCatalog() {
  try {
    const url = `${API_BASE_URL}/api/careers`;
    const response = await fetch(url);
    return await handleResponse(response);
  } catch (error) {
    throw new Error(
      error.message || 'Failed to fetch careers catalog from server.'
    );
  }
}

/**
 * 3. Create a new user profile
 * POST /api/users
 * Payload: { name, education, skills, interests, career_goal }
 */
export async function createUserProfile(profileData) {
  try {
    const url = `${API_BASE_URL}/api/users`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(profileData),
    });
    return await handleResponse(response);
  } catch (error) {
    throw new Error(
      error.message || 'Failed to save profile. Please check your inputs.'
    );
  }
}

/**
 * 4. Retrieve an existing user profile by ID
 * GET /api/users/<user_id>
 */
export async function fetchUserProfile(userId) {
  try {
    const url = `${API_BASE_URL}/api/users/${userId}`;
    const response = await fetch(url);
    return await handleResponse(response);
  } catch (error) {
    throw new Error(
      error.message || `Failed to fetch profile for user #${userId}.`
    );
  }
}

/**
 * 5. Generate career recommendations for a user
 * POST /api/recommend/<user_id>
 */
export async function fetchRecommendations(userId) {
  try {
    const url = `${API_BASE_URL}/api/recommend/${userId}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return await handleResponse(response);
  } catch (error) {
    throw new Error(
      error.message || 'Failed to generate recommendations. Please retry.'
    );
  }
}
