import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

export async function getUserProfile(userId) {
  try {
    const response = await axios.get(`${BASE_URL}/fetch-user/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching user profile: ' + error.message);
  }
}

export async function updateUserProfile(userId, updates) {
  try {
    const response = await axios.post(`${BASE_URL}/update-profile/${userId}`, updates);
    return response.data;
  } catch (error) {
    throw new Error('Error updating user profile: ' + error.message);
  }
}

export async function getUserTeamsDetails(userId) {
  try {
    const response = await axios.get(`${BASE_URL}/fetch-teams/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching user teams: ' + error.message);
  }
}