import { writable } from 'svelte/store';
import { auth } from '../firebase/firebase';
import { onAuthStateChanged } from 'firebase/auth';

export const user = writable(null);

// Listen for auth state changes
onAuthStateChanged(auth, (firebaseUser) => {
  if (firebaseUser) {
    user.set({
      uid: firebaseUser.uid,
      email: firebaseUser.email,
      displayName: firebaseUser.displayName || firebaseUser.email.split('@')[0]
    });
  } else {
    user.set(null);
  }
});