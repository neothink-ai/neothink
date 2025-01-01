<script>
  import { createEventDispatcher } from 'svelte';
  import { updateTask } from '$lib/stores/taskStore';
  import { fade } from 'svelte/transition';
  
  export let task = null; // Make task optional - null means create mode
  export let show = false;
  export let columnId = 'todo'; // Default column for new tasks

  const dispatch = createEventDispatcher();
  let isUpdating = false;
  let error = null;
  
  $: isCreateMode = !task;
  
  $: taskDetails = task ? {
    title: task.title || '',
    priority: task.priority || 'Medium',
    deadline: task.deadline ? new Date(task.deadline).toISOString().slice(0, 16) : '',
    size: task.size || 'Medium',
    assignee: task.assignee || '',
    description: task.description || ''
  } : {
    title: '',
    priority: 'Medium',
    deadline: '',
    size: 'Medium',
    assignee: '',
    description: ''
  };

  function close() {
    error = null;
    dispatch('close');
  }

  async function handleSubmit() {
    isUpdating = true;
    error = null;

    try {
      const updates = {
        ...taskDetails,
        deadline: taskDetails.deadline ? new Date(taskDetails.deadline).toISOString() : null,
        columnId: isCreateMode ? columnId : task.columnId
      };

      if (isCreateMode) {
        dispatch('create', updates);
      } else {
        await updateTask(task.id, updates);
        dispatch('save', updates);
      }
      close();
    } catch (err) {
      error = err.message;
      console.error('Error updating task:', err);
    } finally {
      isUpdating = false;
    }
  }
</script>

{#if show}
  <div class="modal-backdrop" on:click|self={close}>
    <div class="modal-content" role="dialog" aria-modal="true">
      <header class="modal-header">
        <h2>{isCreateMode ? 'Create New Task' : task.title}</h2>
        <button class="close-button" on:click={close}>×</button>
      </header>

      <div class="modal-body">
        {#if error}
          <div class="error-message" transition:fade>
            {error}
          </div>
        {/if}

        <div class="modal-section">
          {#if isCreateMode}
            <div class="form-group">
              <label for="title">Title</label>
              <input 
                type="text" 
                id="title" 
                bind:value={taskDetails.title} 
                placeholder="Enter task title..."
              >
            </div>
            <div class="form-group">
              <label for="columnId">Status</label>
              <select id="columnId" bind:value={columnId}>
                <option value="todo">To Do</option>
                <option value="inProgress">In Progress</option>
                <option value="done">Done</option>
              </select>
            </div>
          {/if}
          <div class="form-grid">
            <div class="form-group">
              <label for="priority">Priority</label>
              <select id="priority" bind:value={taskDetails.priority}>
                <option value="Low">🔽 Low</option>
                <option value="Medium">➡️ Medium</option>
                <option value="High">🔼 High</option>
              </select>
            </div>

            <div class="form-group">
              <label for="size">Size</label>
              <select id="size" bind:value={taskDetails.size}>
                <option value="Small">S</option>
                <option value="Medium">M</option>
                <option value="Large">L</option>
              </select>
            </div>
          </div>
        </div>

        <div class="modal-section">
          <h3>Assignment</h3>
          <div class="form-grid">
            <div class="form-group">
              <label for="assignee">Assignee</label>
              <input 
                type="text" 
                id="assignee" 
                bind:value={taskDetails.assignee} 
                placeholder="Add assignee..."
              >
            </div>

            <div class="form-group">
              <label for="deadline">Deadline</label>
              <input 
                type="datetime-local" 
                id="deadline" 
                bind:value={taskDetails.deadline}
              >
            </div>
          </div>
        </div>

        <div class="modal-section">
          <h3>Description</h3>
          <textarea
            bind:value={taskDetails.description}
            placeholder="Add a description..."
            rows="4"
          ></textarea>
        </div>
      </div>

      <footer class="modal-footer">
        <button 
          class="secondary" 
          on:click={close}
          disabled={isUpdating}
        >
          Cancel
        </button>
        <button 
          class="primary" 
          on:click={handleSubmit}
          disabled={isUpdating || (isCreateMode && !taskDetails.title)}
        >
          {#if isUpdating}
            <span class="spinner"></span>
          {/if}
          {isUpdating ? 'Saving...' : isCreateMode ? 'Create Task' : 'Save Changes'}
        </button>
      </footer>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center; /* Center horizontally */
    align-items: center;    /* Center vertically */
    z-index: 1000;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .modal-content {
    background: #ffffff;
    height: auto;
    width: 480px;
    max-width: 90%;
    display: flex;
    flex-direction: column;
    border-radius: 24px; /* Increased border-radius for more rounded edges */
    overflow: hidden;    /* Ensure inner elements respect rounded corners */
    animation: fadeInModal 0.3s ease-out;
    box-shadow: -8px 0 32px rgba(0, 0, 0, 0.12);
    transform: scale(0.9);
    transition: transform 0.3s ease-out, opacity 0.3s ease-out;
  }

  @keyframes fadeInModal {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
  }

  .modal-header {
    padding: 24px 32px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(to right, #ffffff, #f8fafc);
  }

  .modal-header h2 {
    font-size: 20px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0;
  }

  .modal-body {
    flex: 1;
    padding: 32px;
    overflow-y: auto;
    background: linear-gradient(to bottom right, #ffffff, #fafafa);
  }

  .modal-section {
    margin-bottom: 32px;
    animation: fadeIn 0.4s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .modal-section h3 {
    font-size: 14px;
    font-weight: 600;
    color: #4b5563;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }

  .form-group {
    margin-bottom: 24px;
  }

  label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: #4b5563;
    margin-bottom: 8px;
    transition: color 0.2s ease;
  }

  input, select, textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.2s ease;
    background: #ffffff;
    color: #1f2937;
  }

  input:hover, select:hover, textarea:hover {
    border-color: #d1d5db;
  }

  input:focus, select:focus, textarea:focus {
    border-color: #3b82f6;
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  }

  select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236B7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 16px;
    padding-right: 40px;
  }

  textarea {
    min-height: 120px;
    resize: vertical;
  }

  .modal-footer {
    padding: 24px 32px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    background: linear-gradient(to right, #ffffff, #f8fafc);
  }

  button {
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .primary {
    background: #3b82f6;
    color: white;
    border: none;
  }

  .primary:hover {
    background: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
  }

  .primary:active {
    transform: translateY(0);
  }

  .secondary {
    background: transparent;
    border: none;
    color: #4b5563;
  }

  .secondary:hover {
    background: #f3f4f6;
    color: #1f2937;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 24px;
    color: #6b7280;
    cursor: pointer;
    padding: 8px;
    border-radius: 8px;
    line-height: 1;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: #f3f4f6;
    color: #1f2937;
    transform: rotate(90deg);
  }

  .error-message {
    background: #fef2f2;
    color: #991b1b;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 24px;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid #fecaca;
    animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  }

  @keyframes shake {
    10%, 90% { transform: translateX(-1px); }
    20%, 80% { transform: translateX(2px); }
    30%, 50%, 70% { transform: translateX(-4px); }
    40%, 60% { transform: translateX(4px); }
  }

  .spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
  }

  /* Priority and Size custom styling */
  select[id="priority"] option[value="High"] { color: #dc2626; }
  select[id="priority"] option[value="Medium"] { color: #2563eb; }
  select[id="priority"] option[value="Low"] { color: #059669; }

  /* Add focus state for form groups */
  .form-group:focus-within label {
    color: #3b82f6;
  }

  /* Scrollbar styling */
  .modal-body::-webkit-scrollbar {
    width: 8px;
  }

  .modal-body::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }

  .modal-body::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 4px;
  }

  .modal-body::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
  }
</style>
