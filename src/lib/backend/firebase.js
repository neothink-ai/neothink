import { initializeApp, getApp, getApps } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { firebaseConfig } from './config';

// Initialize Firebase only if it hasn't been initialized
let firebaseApp;
if (!getApps().length) {
  firebaseApp = initializeApp(firebaseConfig);
} else {
  firebaseApp = getApp();
}

// Export auth and firestore instances
export const auth = getAuth(firebaseApp);
export const db = getFirestore(firebaseApp);