import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut, updateProfile
} from 'firebase/auth';
import { auth } from './firebase';
import { goto } from '$app/navigation';

export async function signUp(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // Extract first name from email
    const firstName = email.split('@')[0];

    // Update user profile
    await updateProfile(user, { displayName: firstName });
    goto('/home');
    return userCredential.user;
  } catch (error) {
    throw new Error(error.message);
  }
}

export async function signIn(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    goto('/home');
    return userCredential.user;
  } catch (error) {
    throw new Error(error.message);
  }
}

export async function logOut() {
  try {
    await signOut(auth);
    goto('/');
  } catch (error) {
    throw new Error(error.message);
  }
}
