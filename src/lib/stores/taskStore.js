import { writable } from 'svelte/store';

function createTaskStore() {
    const { subscribe, set, update } = writable([]);

    return {
        subscribe,
        set,
        addTask: (task) => {
            update(tasks => [...tasks, task]);
        },
        updateTask: (id, updates) => {
            update(tasks => 
                tasks.map(task => 
                    task.id === id ? { ...task, ...updates } : task
                )
            );
            return updates; // Return the updates for the UI
        },
        deleteTask: (id) => {
            update(tasks => tasks.filter(task => task.id !== id));
        },
        moveTask: (id, newColumnId) => {
            update(tasks => 
                tasks.map(task => 
                    task.id === id ? { ...task, columnId: newColumnId } : task
                )
            );
        }
    };
}

export const taskStore = createTaskStore();