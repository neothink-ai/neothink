import { writable } from 'svelte/store';
import { getAuth } from 'firebase/auth';

function createTaskStore() {
    const { subscribe, set, update } = writable([]);

    async function requireAuth() {
        const auth = getAuth();
        const user = auth.currentUser;
        if (!user) throw new Error('Authentication required');
        return user;
    }

    return {
        subscribe,
        set,
        addTask: async (taskData) => {
            try {
                const user = await requireAuth();
                const response = await fetch('http://localhost:6876/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ...taskData,
                        userid: user.uid
                    })
                });
                
                if (!response.ok) throw new Error('Failed to add task');
                const newTask = await response.json();
                update(tasks => [...tasks, newTask]);
                return newTask;
            } catch (error) {
                console.error('Failed to add task:', error);
                throw error;
            }
        },
        updateTask: async (id, updates) => {
            try {
                await requireAuth();
                const response = await fetch(`http://localhost:6876/tasks/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updates)
                });
                if (!response.ok) throw new Error('Failed to update task');
                update(tasks => tasks.map(task => 
                    task.id === id ? { ...task, ...updates } : task
                ));
            } catch (error) {
                throw error;
            }
        },
        deleteTask: async (id) => {
            try {
                await requireAuth();
                await fetch(`http://localhost:6876/tasks/${id}`, {
                    method: 'DELETE'
                });
                update(tasks => tasks.filter(task => task.id !== id));
            } catch (error) {
                throw error;
            }
        }
    };
}

export const taskStore = createTaskStore();
export const { addTask, updateTask, deleteTask } = taskStore;