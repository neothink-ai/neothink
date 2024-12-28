<script>
  import { createEventDispatcher } from 'svelte';
  
  export let task;
  export let onEditTask;
  export let onDeleteTask;

  const dispatch = createEventDispatcher();
  let isEditing = false;
  let editedTitle = task.title;
  let isDragging = false;
  let showModal = false;

  // New task details
  let taskDetails = {
    priority: task.priority || 'Medium',
    deadline: task.deadline || '',
    size: task.size || 'Medium',
    assignee: task.assignee || '',
  };

  function toggleModal() {
    showModal = !showModal;
  }

  function saveTaskDetails() {
    dispatch('updateTask', {
      ...task,
      ...taskDetails
    });
    toggleModal();
  }

  function handleDragStart(event) {
    const taskData = {
      id: task.id,
      title: task.title,
      columnId: task.columnId,
      priority: task.priority,
      size: task.size,
      deadline: task.deadline,
      assignee: task.assignee
    };
    
    event.dataTransfer.setData('application/json', JSON.stringify(taskData));
    event.dataTransfer.effectAllowed = 'move';
    event.target.classList.add('is-dragging');
  }

  function handleDragEnd(event) {
    event.target.classList.remove('is-dragging');
  }

  function saveEdit() {
    if (editedTitle.trim()) {
      onEditTask(task.id, editedTitle);
      isEditing = false;
    }
  }

  function cancelEdit() {
    editedTitle = task.title;
    isEditing = false;
  }

  function handleDelete(event) {
    event.stopPropagation(); // Prevent event bubbling
    onDeleteTask(task.id);
  }
</script>

<!-- Add modal markup -->
{#if showModal}
  <div class="modal-backdrop" on:click|self={toggleModal}>
    <div class="modal">
      <h3>Task Details</h3>
      <div class="form-group">
        <label for="priority">Priority</label>
        <select bind:value={taskDetails.priority}>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      <div class="form-group">
        <label for="deadline">Deadline</label>
        <input type="datetime-local" bind:value={taskDetails.deadline}>
      </div>

      <div class="form-group">
        <label for="size">Size</label>
        <select bind:value={taskDetails.size}>
          <option value="Small">Small</option>
          <option value="Medium">Medium</option>
          <option value="Large">Large</option>
        </select>
      </div>

      <div class="form-group">
        <label for="assignee">Assignee</label>
        <input type="text" bind:value={taskDetails.assignee}>
      </div>

      <div class="modal-actions">
        <button on:click={saveTaskDetails}>Save</button>
        <button on:click={toggleModal}>Cancel</button>
      </div>
    </div>
  </div>
{/if}

<li
  class="task {isDragging ? 'is-dragging' : ''}"
  draggable="true"
  on:dragstart={handleDragStart}
  on:dragend={handleDragEnd}
  data-task-id={task.id}
>
  {#if isEditing}
    <input 
      bind:value={editedTitle} 
      on:blur={saveEdit} 
      on:keyup="{e => e.key === 'Enter' && saveEdit()}"
    />
    <button on:click|stopPropagation={cancelEdit}>Cancel</button>
  {:else}
    <span on:dblclick|stopPropagation={() => isEditing = true}>{task.title}</span>
    <div class="task-actions">
      <button 
        class="delete-button"
        on:click={handleDelete}
        title="Delete task"
      >
        Delete
      </button>
      <button class="details-button" on:click={toggleModal}>Details</button>
    </div>
  {/if}
</li>

<style>
  .task {
    background-color: #fff;
    padding: 12px;
    margin-bottom: 8px;
    border-radius: 3px;
    box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25);
    cursor: grab;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 
      background-color 0.2s ease,
      transform 0.1s ease,
      box-shadow 0.1s ease;
    border: 2px solid transparent;
    user-select: none;
    transform-origin: center;
  }
  .task:hover {
    background-color: #f4f5f7;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(9, 30, 66, 0.15);
  }
  .task.is-dragging {
    opacity: 0.9;
    transform: scale(1.02);
    box-shadow: 0 8px 16px rgba(9, 30, 66, 0.25);
    background: #fff;
    cursor: grabbing;
  }
  .task:active {
    cursor: grabbing;
    transform: scale(1.02);
  }
  input {
    flex: 1;
    margin-right: 8px;
    padding: 6px 8px;
    border: 2px solid #4c9aff;
    border-radius: 3px;
    font-size: 14px;
    background: white;
    box-shadow: 0 0 0 2px rgba(76, 154, 255, 0.2);
  }
  input:focus {
    outline: none;
  }
  button {
    padding: 4px 8px;
    background: transparent;
    border: none;
    color: #42526e;
    cursor: pointer;
    border-radius: 3px;
    font-size: 12px;
    transition: all 0.15s ease;
  }
  button:hover {
    color: #FF5630;
    background: rgba(255, 86, 48, 0.08);
  }
  span {
    font-size: 14px;
    color: #172b4d;
    flex: 1;
    padding: 2px 4px;
  }

  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: white;
    padding: 20px;
    border-radius: 8px;
    min-width: 300px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
  }

  .form-group input,
  .form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }

  .details-button {
    margin-left: 8px;
    padding: 4px 8px;
    background: transparent;
    border: none;
    color: #42526e;
    cursor: pointer;
    border-radius: 3px;
  }

  .details-button:hover {
    background: rgba(9, 30, 66, 0.08);
  }

  .task-actions {
    display: flex;
    gap: 8px;
  }
</style>
