<script>
    import { user } from '$lib/stores/userStore';
    import { taskStore } from '$lib/stores/taskStore';
    import { fade, slide } from 'svelte/transition';

    let projectDescription = '';
    let generatedTasks = [];
    let loading = false;
    let error = null;

    async function generateTasks() {
        if (!projectDescription.trim()) return;
        
        loading = true;
        error = null;
        
        try {
            const response = await fetch('http://localhost:6876/tasker/generate-tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project_description: projectDescription,
                    userid: $user.uid
                })
            });

            if (!response.ok) throw new Error('Failed to generate tasks');
            
            const data = await response.json();
            generatedTasks = data.tasks;
        } catch (err) {
            error = err.message;
            console.error('Error:', err);
        } finally {
            loading = false;
        }
    }

    async function acceptTasks() {
        try {
            const response = await fetch('http://localhost:6876/tasker/accept-neoplan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_ids: generatedTasks.map(t => t._id),
                    userid: $user.uid
                })
            });

            if (!response.ok) throw new Error('Failed to accept tasks');
            
            const data = await response.json();
            generatedTasks = [];
            projectDescription = '';
            
            // Refresh the task list
            await taskStore.loadTasks($user.uid);
        } catch (err) {
            error = err.message;
            console.error('Error:', err);
        }
    }
</script>

<div class="task-generator" in:fade>
    <h2>AI Task Generator</h2>
    
    <div class="input-section">
        <textarea
            bind:value={projectDescription}
            placeholder="Describe your project and I'll help break it down into tasks..."
            rows="4"
        ></textarea>
        
        <button 
            on:click={generateTasks}
            disabled={loading || !projectDescription.trim()}
            class="generate-btn"
        >
            {loading ? 'Generating...' : 'Generate Tasks'}
        </button>
    </div>

    {#if error}
        <div class="error" transition:slide>{error}</div>
    {/if}

    {#if generatedTasks.length > 0}
        <div class="generated-tasks" in:slide>
            <h3>Generated Tasks</h3>
            <div class="task-list">
                {#each generatedTasks as task}
                    <div class="task-card">
                        <h4>{task.title}</h4>
                        <p>{task.description}</p>
                        <div class="task-meta">
                            <span class="priority {task.priority.toLowerCase()}">{task.priority}</span>
                            <span class="size">{task.size}</span>
                        </div>
                    </div>
                {/each}
            </div>
            <button class="accept-btn" on:click={acceptTasks}>
                Accept All Tasks
            </button>
        </div>
    {/if}
</div>

<style>
    .task-generator {
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .input-section {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        resize: vertical;
    }

    .generate-btn {
        padding: 12px;
        background: #0052cc;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.2s;
    }

    .generate-btn:disabled {
        background: #ccc;
        cursor: not-allowed;
    }

    .task-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }

    .task-card {
        padding: 16px;
        background: #f4f5f7;
        border-radius: 4px;
        border: 1px solid #ddd;
    }

    .task-meta {
        display: flex;
        gap: 8px;
        margin-top: 8px;
    }

    .priority {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
    }

    .priority.high { background: #ffebe6; color: #de350b; }
    .priority.medium { background: #fffae6; color: #ff991f; }
    .priority.low { background: #e3fcef; color: #006644; }

    .size {
        padding: 2px 8px;
        background: #deebff;
        color: #0747a6;
        border-radius: 12px;
        font-size: 12px;
    }

    .accept-btn {
        width: 100%;
        padding: 12px;
        background: #36b37e;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.2s;
    }

    .accept-btn:hover {
        background: #2d995b;
    }

    .error {
        padding: 12px;
        background: #ffebe6;
        color: #de350b;
        border-radius: 4px;
        margin: 10px 0;
    }
</style>
