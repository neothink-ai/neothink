<script>
  import { createEventDispatcher } from 'svelte';
  import { taskStore } from '$lib/stores/taskStore';
  import { fade } from 'svelte/transition';
  
  export let task;
  export let show = false;
  export let onAddTask;
  let title = '';
  let columnId = 'todo';

  const dispatch = createEventDispatcher();
  let isUpdating = false;
  let error = null;
  
  let taskDetails = {
    title: task.title || '',
    priority: task.priority || 'Medium',
    deadline: task.deadline ? new Date(task.deadline).toISOString().slice(0, 16) : '',
    size: task.size || 'Medium',
    assignee: task.assignee || '',
    description: task.description || ''
  };

  function close() {
    error = null;
    dispatch('close');
  }

  async function saveChanges() {
    isUpdating = true;
    error = null;

    try {
      const updates = {
        ...taskDetails,
        deadline: taskDetails.deadline ? new Date(taskDetails.deadline).toISOString() : null,
        columnId: task.columnId // Ensure columnId is included
      };

      const updatedTask = taskStore.updateTask(task.id, updates);
      dispatch('taskUpdated', updatedTask);
      close();
    } catch (err) {
      error = err.message;
      console.error('Error updating task:', err);
    } finally {
      isUpdating = false;
    }
  }

  function handleSubmit() {
    onAddTask(title, columnId);
    title = '';
  }
</script>

{#if show}
  <div class="modal-backdrop" on:click|self={close}>
    <div class="modal-content" role="dialog" aria-modal="true">
      <header class="modal-header">
        <h2>{task.title}</h2>
        <button class="close-button" on:click={close}>×</button>
      </header>

      <div class="modal-body">
        {#if error}
          <div class="error-message" transition:fade>
            {error}
          </div>
        {/if}

        <div class="modal-section">
          <h3>Details</h3>
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
          on:click={saveChanges}
          disabled={isUpdating}
        >
          {#if isUpdating}
            <span class="spinner"></span>
          {/if}
          {isUpdating ? 'Saving...' : 'Save Changes'}
        </button>
      </footer>
    </div>
  </div>
{/if}

<div class="modal">
  <input type="text" bind:value={title} placeholder="Task title" />
  <select bind:value={columnId}>
    <option value="todo">To Do</option>
    <option value="inProgress">In Progress</option>
    <option value="done">Done</option>
  </select>
  <button on:click={handleSubmit}>Add Task</button>
</div>

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: flex-end;
    z-index: 1000;
  }

  .modal-content {
    background: white;
    height: 100%;
    width: 480px;
    display: flex;
    flex-direction: column;
    animation: slideIn 0.2s ease-out;
  }

  @keyframes slideIn {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
  }

  .modal-header {
    padding: 16px 24px;
    border-bottom: 1px solid #dfe1e6;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-body {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
  }

  .modal-footer {
    padding: 16px 24px;
    border-top: 1px solid #dfe1e6;
    display: flex;
    justify-content: flex-end;
    gap: 8px;
  }

  .modal-section {
    margin-bottom: 24px;
  }

  .modal-section h3 {
    font-size: 14px;
    color: #6b778c;
    margin-bottom: 8px;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  label {
    display: block;
    font-size: 12px;
    font-weight: 500;
    color: #6b778c;
    margin-bottom: 4px;
  }

  input, select, textarea {
    width: 100%;
    padding: 8px;
    border: 2px solid #dfe1e6;
    border-radius: 3px;
    font-size: 14px;
    transition: all 0.2s;
  }

  input:focus, select:focus, textarea:focus {
    border-color: #4c9aff;
    outline: none;
    box-shadow: 0 0 0 2px rgba(76, 154, 255, 0.2);
  }

  button {
    padding: 8px 16px;
    border-radius: 3px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .primary {
    background: #0052cc;
    color: white;
    border: none;
  }

  .primary:hover {
    background: #0047b3;
  }

  .secondary {
    background: transparent;
    border: none;
    color: #42526e;
  }

  .secondary:hover {
    background: rgba(9, 30, 66, 0.08);
  }

  .close-button {
    background: none;
    border: none;
    font-size: 24px;
    color: #42526e;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 3px;
  }

  .close-button:hover {
    background: rgba(9, 30, 66, 0.08);
  }

  .error-message {
    background: #ffebe6;
    color: #de350b;
    padding: 8px 12px;
    border-radius: 3px;
    margin-bottom: 16px;
    font-size: 14px;
  }

  .spinner {
    display: inline-block;
    width: 12px;
    height: 12px;
    border: 2px solid #ffffff;
    border-top-color: transparent;
    border-radius: 50%;
    margin-right: 8px;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .modal {
    padding: 16px;
    background: #fff;
    border: 1px solid #ddd;
  }
</style>
