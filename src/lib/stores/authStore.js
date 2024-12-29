import { writable } from 'svelte/store';
import { auth } from '../firebase/firebase';

// Create store without immediately attaching listener
const authStore = writable({
    user: null,
    loading: true,
    error: null
});

export { authStore };
