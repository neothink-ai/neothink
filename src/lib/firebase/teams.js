import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

import { collection, query, where, getDocs, addDoc, deleteDoc, doc, updateDoc } from 'firebase/firestore';
import { db } from './firebase';

// Remove getUserTeams function

export async function getAllTeams() {
  try {
    const response = await axios.get(`${BASE_URL}/fetch-all-teams`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching all teams: ' + error.message);
  }
}

export async function addMemberToTeam(teamId, userId) {
  try {
    const response = await axios.post(`${BASE_URL}/add-user-to-team/${teamId}/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error('Error adding member to team: ' + error.message);
  }
}

export async function removeMemberFromTeam(teamId, userId) {
  try {
    const response = await axios.post(`${BASE_URL}/remove-user-from-team/${teamId}/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error('Error removing member from team: ' + error.message);
  }
}