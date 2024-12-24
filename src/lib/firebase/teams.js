import { collection, query, where, getDocs, addDoc, deleteDoc, doc, updateDoc } from 'firebase/firestore';
import { db } from './firebase';

export async function getUserTeams(userId) {
  try {
    const q = query(
      collection(db, 'teams'),
      where('members', 'array-contains', userId)
    );
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    throw new Error('Error fetching user teams: ' + error.message);
  }
}

export async function getAllTeams() {
  try {
    const snapshot = await getDocs(collection(db, 'teams'));
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    throw new Error('Error fetching all teams: ' + error.message);
  }
}

export async function addMemberToTeam(teamId, userId) {
  try {
    const teamRef = doc(db, 'teams', teamId);
    await updateDoc(teamRef, {
      members: arrayUnion(userId)
    });
  } catch (error) {
    throw new Error('Error adding member to team: ' + error.message);
  }
}

export async function removeMemberFromTeam(teamId, userId) {
  try {
    const teamRef = doc(db, 'teams', teamId);
    await updateDoc(teamRef, {
      members: arrayRemove(userId)
    });
  } catch (error) {
    throw new Error('Error removing member from team: ' + error.message);
  }
}