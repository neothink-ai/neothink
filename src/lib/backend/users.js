import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export async function getUserProfile(userId) {
  try {
    // console.log("Sending fetch-user request: ")
    const response = await axios.get(`${BASE_URL}/fetch-user/${userId}`);
    let return_data = JSON.parse(response.data);
    return return_data;
  } catch (error) {
    throw new Error('Error fetching user profile: ' + error.message);
  }
}

export async function updateUserProfile(userId, updates) {
  try {
    // console.log(typeof(updates));
    // console.log(updates);
    const response = await axios.post(`${BASE_URL}/update-profile/${userId}`, updates);
    // console.log(response)
    let return_data = response.data;
    return return_data;
  } catch (error) {
    throw new Error('Error updating user profile: ' + error.message);
  }
}

export async function getUserTeamsDetails(userId) {
  try {
    // console.log("Getting fetch-teams request: ")
    const response = await axios.get(`${BASE_URL}/fetch-teams/${userId}`);
    let return_data = JSON.parse(response.data);
    return return_data;
  } catch (error) {
    throw new Error('Error fetching user teams: ' + error.message);
  }
}

export async function getUserTasks(userId) {
  try {
    const response = await axios.get(`${BASE_URL}/fetch-tasks/${userId}`);
    let return_data = JSON.parse(response.data);
    return return_data;
  } catch (error) {
    throw new Error('Error fetching user tasks: ' + error.message);
  }
}

export async function getUserTasksForDate(userId, date) {
  try {
    const response = await axios.get(`${BASE_URL}/fetch-task-on-date/${userId}/${date}`);
    let return_data = JSON.parse(response.data);
    return return_data;
  } catch (error) {
    throw new Error('Error fetching user tasks for date: ' + error.message);
  }
}