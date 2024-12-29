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
        setTasks: (tasks) => {
            update(state => tasks);
        },
        addTask: async (taskData) => {
            try {
                const user = await requireAuth();
                const now = new Date().toISOString();
                
                // Ensure all required fields are present with proper types
                const fullTaskData = {
                    title: String(taskData.title || ''),
                    columnId: String(taskData.columnId || 'todo'),
                    userid: String(user.uid),
                    state: String(taskData.state || taskData.columnId || 'todo'),
                    priority: String(taskData.priority || 'Medium'),
                    size: String(taskData.size || 'Medium'),
                    description: String(taskData.description || ''),
                    deadline: taskData.deadline || null,
                    assignee: taskData.assignee || null,
                    assigned_time: now,
                    completed_time: null
                };

                const response = await fetch('http://localhost:6876/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(fullTaskData)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(typeof errorData.detail === 'string' 
                        ? errorData.detail 
                        : 'Failed to add task');
                }

                const newTask = await response.json();
                
                const processedTask = {
                    id: newTask._id.$oid,
                    ...fullTaskData
                };

                update(tasks => [...tasks, processedTask]);
                return processedTask;
            } catch (error) {
                console.error('Failed to add task:', error);
                throw new Error(error.message || 'Failed to add task');
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