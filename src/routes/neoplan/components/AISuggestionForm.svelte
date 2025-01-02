<script>
    import { createEventDispatcher } from 'svelte';
    import { user } from '$lib/stores/userStore';
    
    const dispatch = createEventDispatcher();
    
    let description = '';
    let loading = false;
    let error = null;

    async function handleSubmit() {
        if (!description.trim() || !$user) return;
        
        loading = true;
        error = null;
        
        try {
            console.log('Sending request with data:', {
                project_description: description,
                userid: $user.uid
            });

            const response = await fetch('http://localhost:6876/tasker/generate-tasks', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    project_description: description,
                    userid: $user.uid
                })
            });

            const contentType = response.headers.get('content-type');
            const data = contentType?.includes('application/json') 
                ? await response.json() 
                : await response.text();
            
            console.log('Response status:', response.status);
            console.log('Response data:', data);

            if (!response.ok) {
                throw new Error(typeof data === 'string' ? data : JSON.stringify(data));
            }
            
            if (data.tasks) {
                dispatch('tasksGenerated', data.tasks);
                description = '';
            } else {
                throw new Error('No tasks received from server');
            }
        } catch (err) {
            error = err.message;
            console.error('Error:', err);
        } finally {
            loading = false;
        }
    }
</script>

<div class="suggestion-form">
    <h2>AI Task Generator</h2>
    
    {#if error}
        <div class="error-message">{error}</div>
    {/if}
    
    <div class="input-container">
        <textarea
            bind:value={description}
            placeholder="Describe your project and I'll help break it down into tasks..."
            rows="4"
            disabled={loading}
        ></textarea>
        
        <button 
            on:click={handleSubmit}
            disabled={loading || !description.trim()}
            class:loading
        >
            {loading ? 'Generating...' : 'Generate Tasks'}
        </button>
    </div>
</div>

<style>
    .suggestion-form {
        background: white;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    h2 {
        margin: 0 0 16px 0;
        color: #172b4d;
    }

    .input-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    textarea {
        width: 100%;
        padding: 12px;
        border: 2px solid #dfe1e6;
        border-radius: 4px;
        resize: vertical;
        font-size: 14px;
        transition: border-color 0.2s ease;
    }

    textarea:focus {
        border-color: #4c9aff;
        outline: none;
    }

    button {
        padding: 12px 24px;
        background: #0052cc;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 500;
        transition: background 0.2s ease;
    }

    button:hover:not(:disabled) {
        background: #0747a6;
    }

    button:disabled {
        background: #dfe1e6;
        cursor: not-allowed;
    }

    button.loading {
        background: #0052cc;
        opacity: 0.7;
    }

    .error-message {
        padding: 12px;
        background: #ffebe6;
        color: #de350b;
        border-radius: 4px;
        margin-bottom: 16px;
    }
</style>
