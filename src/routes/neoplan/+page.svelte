<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import { user } from '$lib/stores/userStore';
    import { fade, slide } from 'svelte/transition';
    import TaskBall from './components/TaskBall.svelte';
    import AISuggestionForm from './components/AISuggestionForm.svelte';
    import CommonLayout from '../CommonLayout.svelte';

    let projectDescription = '';
    let generatedTasks = [];
    let selectedTasks = new Set();
    const dispatch = createEventDispatcher();

    async function generateTasks(description) {
        const response = await fetch('http://localhost:8000/tasker/generate-tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ project_description: description, userid: 'user123' })
        });

        if (!response.ok) {
            throw new Error('Failed to generate tasks');
        }

        return await response.json();
    }

    async function handleGenerateTasks() {
        try {
            const response = await generateTasks(projectDescription);
            generatedTasks = response.task_ids;
        } catch (error) {
            console.error('Error generating tasks:', error);
        }
    }

    async function acceptNeoplan() {
        try {
            const response = await fetch('http://localhost:8000/tasker/accept-neoplan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task_ids: generatedTasks, userid: 'user123' })
            });

            if (!response.ok) {
                throw new Error('Failed to accept neoplan');
            }

            const result = await response.json();
            dispatch('tasksAccepted', result);
        } catch (error) {
            console.error('Error accepting neoplan:', error);
        }
    }

    function handleTasksGenerated(event) {
        generatedTasks = event.detail;
    }

    function toggleTaskSelection(taskId) {
        if (selectedTasks.has(taskId)) {
            selectedTasks.delete(taskId);
        } else {
            selectedTasks.add(taskId);
        }
        selectedTasks = selectedTasks; // trigger reactivity
    }

    async function acceptSelectedTasks() {
        try {
            const response = await fetch('http://localhost:6876/tasker/accept-neoplan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_ids: Array.from(selectedTasks),
                    userid: $user.uid
                })
            });

            if (!response.ok) throw new Error('Failed to accept tasks');
            
            generatedTasks = [];
            selectedTasks.clear();
            
        } catch (error) {
            console.error('Error accepting tasks:', error);
        }
    }
</script>

<CommonLayout pageType="neoplan">
    <div class="neoplan-page">
        <div class="logo-container">
            <img 
                src="src\lib\assets\neoplan-logo.png" 
                alt="NeoPlan"
                class="logo"
            />
        </div>

        {#if $user}
            <div class="content" in:fade>
                <div class="header-section">
                    <h1>AI Project Planner</h1>
                    <p class="subtitle">Transform your project ideas into structured tasks using AI</p>
                </div>

                <div class="planner-grid">
                    <div class="input-section">
                        <AISuggestionForm on:tasksGenerated={handleTasksGenerated} />
                    </div>

                    {#if generatedTasks.length > 0}
                        <div class="tasks-section" in:slide>
                            <div class="tasks-header">
                                <h2>Generated Tasks</h2>
                                <span class="task-count">{generatedTasks.length} tasks</span>
                            </div>

                            <div class="task-grid">
                                {#each generatedTasks as task, i}
                                    <div 
                                        class="task-wrapper"
                                        class:selected={selectedTasks.has(task._id)}
                                        in:fade={{delay: i * 50}}
                                    >
                                        <TaskBall 
                                            {task} 
                                            index={i}
                                            on:click={() => toggleTaskSelection(task._id)}
                                        />
                                    </div>
                                {/each}
                            </div>
                            
                            {#if selectedTasks.size > 0}
                                <div class="actions-bar" in:slide>
                                    <span class="selected-count">
                                        {selectedTasks.size} tasks selected
                                    </span>
                                    <button 
                                        class="accept-button"
                                        on:click={acceptSelectedTasks}
                                    >
                                        <i class="fas fa-check"></i>
                                        Add to Kanban Board
                                    </button>
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>
            </div>
        {:else}
            <div class="login-prompt" in:fade>
                <i class="fas fa-lock"></i>
                <h2>Authentication Required</h2>
                <p>Please log in to use the AI Project Planner</p>
            </div>
        {/if}
    </div>
</CommonLayout>

<style>
    .neoplan-page {
        /* Remove min-height: 100vh as it's handled by CommonLayout */
        background: #f4f5f7;
        padding: 0 0 32px 0;
    }

    .logo-container {
        padding: 16px 24px;
        background: white;
        box-shadow: 0 1px 0 rgba(9, 30, 66, 0.08);
        margin-bottom: 32px;
    }

    .logo {
        height: 32px;
        width: auto;
        opacity: 0.95;
        transition: opacity 0.2s ease;
    }

    .header-section {
        text-align: center;
        margin-bottom: 48px;
    }

    h1 {
        font-size: 32px;
        font-weight: 600;
        color: #172b4d;
        margin: 0 0 8px 0;
    }

    .subtitle {
        color: #5e6c84;
        font-size: 16px;
        margin: 0;
    }

    .planner-grid {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
        display: grid;
        gap: 32px;
    }

    .tasks-section {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        padding: 24px;
    }

    .tasks-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }

    .task-count {
        background: #ebecf0;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 14px;
        color: #42526e;
    }

    .task-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 24px;
        margin-bottom: 24px;
    }

    .task-wrapper {
        position: relative;
    }

    .task-wrapper.selected::after {
        content: '✓';
        position: absolute;
        top: -8px;
        right: -8px;
        background: #36B37E;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(54, 179, 126, 0.3);
    }

    .actions-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px;
        background: #f8f9fa;
        border-radius: 8px;
        margin-top: 24px;
    }

    .selected-count {
        color: #42526e;
        font-size: 14px;
    }

    .accept-button {
        background: #36B37E;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }

    .accept-button:hover {
        background: #2d995b;
        transform: translateY(-1px);
    }

    .login-prompt {
        text-align: center;
        padding: 48px 24px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 64px auto;
    }

    .login-prompt i {
        font-size: 24px;
        color: #42526e;
        margin-bottom: 16px;
    }

    @media (max-width: 768px) {
        .planner-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
