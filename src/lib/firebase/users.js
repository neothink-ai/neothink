import { doc, getDoc, updateDoc, collection, query, where, getDocs } from 'firebase/firestore';
import { db } from './firebase';

export async function getUserProfile(uid) {
  try {
    const userDoc = await getDoc(doc(db, 'users', uid));
    if (!userDoc.exists()) {
      throw new Error('User not found');
    }
    return { id: userDoc.id, ...userDoc.data() };
  } catch (error) {
    throw new Error('Error fetching user profile: ' + error.message);
  }
}

export async function updateUserProfile(uid, updates) {
  try {
    const allowedUpdates = ['firstName', 'lastName', 'skills'];
    const filteredUpdates = Object.keys(updates)
      .filter(key => allowedUpdates.includes(key))
      .reduce((obj, key) => {
        obj[key] = updates[key];
        return obj;
      }, {});

    await updateDoc(doc(db, 'users', uid), filteredUpdates);
  } catch (error) {
    throw new Error('Error updating user profile: ' + error.message);
  }
}

export async function getUserTeamsDetails(teamIds) {
  try {
    const teamsRef = collection(db, 'teams');
    const teamsQuery = query(teamsRef, where('__name__', 'in', teamIds));
    const snapshot = await getDocs(teamsQuery);
    return snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    throw new Error('Error fetching user teams: ' + error.message);
  }
}