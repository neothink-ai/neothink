import { writable } from 'svelte/store';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../backend/firebase'; // Import your Firebase auth instance

const tempUser = writable(null);

// Initialize user from localStorage if available
if (typeof window !== 'undefined') {
  console.log('userStore.js: window is defined');
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    console.log("loaded user from memory");``
    tempUser.set(JSON.parse(storedUser));
  }
}

// Subscribe to Firebase auth changes
onAuthStateChanged(auth, (firebaseUser) => {
  if(!tempUser){ 
    if (firebaseUser) {
      const userData = {
        uid: firebaseUser.uid,
        email: firebaseUser.email,
        displayName: firebaseUser.displayName || firebaseUser.email.split('@')[0],
      };

      // Update the store and localStorage
      tempUser.set(userData);
      if (typeof window !== 'undefined') {
        console.log("Obtained data from firebase. commiting to local storage");
        localStorage.setItem('user', JSON.stringify(userData));
      }
    } else {
      // Clear the store and localStorage on logout
      tempUser.set(null);
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
      }
    }
  }
  // Set loading to false after determining auth state
  isLoading.set(false);
});

// Create writable stores
export const user = tempUser;
export const isLoading = writable(true);