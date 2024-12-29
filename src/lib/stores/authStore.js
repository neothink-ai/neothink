import { writable } from 'svelte/store';
import { getAuth, onAuthStateChanged } from 'firebase/auth';

function createAuthStore() {
    const { subscribe, set, update } = writable({
        user: null,
        loading: true,
        error: null
    });

    const auth = getAuth();

    onAuthStateChanged(auth, (user) => {
        if (user) {
            set({ user, loading: false, error: null });
        } else {
            set({ user: null, loading: false, error: null });
        }
    });

    return {
        subscribe,
        setError: (error) => update(state => ({ ...state, error }))
    };
}

export const authStore = createAuthStore();
