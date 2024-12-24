// src/lib/stores/authStore.js
import { writable } from "svelte/store";
import { auth } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";

export const user = writable(null);
export const loading = writable(true);
export const error = writable(null);

// Setup auth state listener
onAuthStateChanged(auth, (userData) => {
  user.set(userData);
  loading.set(false);
});

export const authHandlers = {
  signup: async (email, password) => {
    try {
      error.set(null);
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );
      return userCredential.user;
    } catch (err) {
      error.set(err.message);
      throw err;
    }
  },

  login: async (email, password) => {
    try {
      error.set(null);
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      return userCredential.user;
    } catch (err) {
      error.set(err.message);
      throw err;
    }
  },

  logout: async () => {
    try {
      await signOut(auth);
      user.set(null);
    } catch (err) {
      error.set(err.message);
      throw err;
    }
  },

  // Google SignUp using OAuth
  signupWithGoogle: async () => {
    const provider = new GoogleAuthProvider();
    try {
      error.set(null);
      const result = await signInWithPopup(auth, provider);
      return result.user;
    } catch (err) {
      error.set(err.message);
      console.error("Google authentication failed", err); // Added error logging
      throw err;
    }
  },
};
