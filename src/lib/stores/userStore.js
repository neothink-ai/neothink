import { writable } from 'svelte/store';
import { auth } from '../backend/firebase';
import { onAuthStateChanged } from 'firebase/auth';

export const user = writable(null);
export const isLoading = writable(true); // Initialize isLoading to true

// Use the singleton auth instance
const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
  if (firebaseUser) {
    user.set({
      uid: firebaseUser.uid,
      email: firebaseUser.email,
      displayName: firebaseUser.displayName || firebaseUser.email.split('@')[0]
    });
  } else {
    user.set(null);
  }
  isLoading.set(false); // Set isLoading to false after the user state is determined
});

// Cleanup subscription on app unmount
if (import.meta.hot) {
  import.meta.hot.dispose(() => {
    unsubscribe();
  });
}