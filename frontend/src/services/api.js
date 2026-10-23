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
 * Shared GET helper with a friendly fallback error message.
 */
async function getJson(path, fallbackMessage) {
  try {
    const url = path === '/' ? (API_BASE_URL || '/') : `${API_BASE_URL}${path}`;
    const response = await fetch(url);
    return await handleResponse(response);
  } catch (error) {
    throw new Error(error.message || fallbackMessage);
  }
}

/**
 * Shared POST helper that always sends JSON.
 */
async function postJson(path, body, fallbackMessage) {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {}),
    });
    return await handleResponse(response);
  } catch (error) {
    throw new Error(error.message || fallbackMessage);
  }
}

/**
 * 1. Check API health & status
 * GET /
 */
export async function checkApiHealth() {
  return getJson('/', 'Unable to connect to backend server. Please verify Flask is running.');
}

/**
 * 2. Fetch available careers catalog and their required skills
 * GET /api/careers
 * @param {Object} options - { view: 'summary', category: 'Cybersecurity' }
 */
export async function fetchCareersCatalog(options = {}) {
  const params = new URLSearchParams();
  if (options.view) params.set('view', options.view);
  if (options.category) params.set('category', options.category);
  const query = params.toString() ? `?${params.toString()}` : '';

  return getJson(`/api/careers${query}`, 'Failed to fetch careers catalog from server.');
}

/**
 * 3. Fetch one career with its full role progression ladder
 * GET /api/careers/<career_id>
 */
export async function fetchCareerDetail(careerId) {
  return getJson(`/api/careers/${careerId}`, `Failed to fetch details for ${careerId}.`);
}

/**
 * 4. Knowledge base stats, algorithm description and in-demand skills
 * GET /api/stats
 */
export async function fetchKnowledgeBaseStats() {
  return getJson('/api/stats', 'Failed to fetch knowledge base statistics.');
}

/**
 * 5. Skill catalog grouped by category (difficulty, hours, prerequisites)
 * GET /api/skills
 */
export async function fetchSkillCatalog() {
  return getJson('/api/skills', 'Failed to fetch the skill catalog.');
}

/**
 * 6. Grouped interest catalog for the profile form
 * GET /api/interests
 */
export async function fetchInterestCatalog() {
  return getJson('/api/interests', 'Failed to fetch the interest catalog.');
}

/**
 * 7. Education dropdown options
 * GET /api/education-options
 */
export async function fetchEducationOptions() {
  return getJson('/api/education-options', 'Failed to fetch education options.');
}

/**
 * 8. Create a new user profile
 * POST /api/users
 * Payload: { name, education, skills, interests, career_goal, hours_per_week }
 */
export async function createUserProfile(profileData) {
  return postJson('/api/users', profileData, 'Failed to save profile. Please check your inputs.');
}

/**
 * 9. Retrieve an existing user profile by ID
 * GET /api/users/<user_id>
 */
export async function fetchUserProfile(userId) {
  return getJson(`/api/users/${userId}`, `Failed to fetch profile for user #${userId}.`);
}

/**
 * 10. Generate ranked career recommendations with generated career paths
 * POST /api/recommend/<user_id>
 * @param {Object} options - { top_n: 3, hours_per_week: 10 }
 */
export async function fetchRecommendations(userId, options = {}) {
  return postJson(
    `/api/recommend/${userId}`,
    options,
    'Failed to generate recommendations. Please retry.'
  );
}

/**
 * 11. Generate the career path for one specific career
 * POST /api/career-path/<user_id>/<career_id>
 */
export async function fetchCareerPath(userId, careerId, options = {}) {
  return postJson(
    `/api/career-path/${userId}/${careerId}`,
    options,
    `Failed to generate the career path for ${careerId}.`
  );
}

/**
 * 12. Compare several careers side by side for one profile
 * POST /api/compare/<user_id>
 */
export async function compareCareerPaths(userId, careerIds, options = {}) {
  return postJson(
    `/api/compare/${userId}`,
    { career_ids: careerIds, ...options },
    'Failed to compare the selected careers.'
  );
}

/**
 * 13. Instant analysis without saving a profile
 * POST /api/analyze
 */
export async function analyzeProfile(profileData) {
  return postJson('/api/analyze', profileData, 'Failed to analyze the profile.');
}
