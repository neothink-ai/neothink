<script>
  import { createEventDispatcher } from 'svelte';
  import TaskModal from './TaskModal.svelte';
  
  export let task;
  export let onEditTask = () => {};  // Default no-op function
  export let onDeleteTask = () => {};  // Default no-op function

  const dispatch = createEventDispatcher();
  let isEditing = false;
  let editedTitle = task.title;
  let isDragging = false;
  let showModal = false;

  function handleTaskUpdate(event) {
    dispatch('updateTask', {
      ...task,
      ...event.detail
    });
  }

  function handleDragStart(event) {
    const taskData = {
      id: task.id,
      title: task.title,
      columnId: task.columnId,
      userid: task.userid,
      state: task.state,
      priority: task.priority,
      size: task.size,
      description: task.description,
      deadline: task.deadline,
      assignee: task.assignee,
      assigned_time: task.assigned_time,
      completed_time: task.completed_time
    };
    
    event.dataTransfer.setData('application/json', JSON.stringify(taskData));
    event.dataTransfer.effectAllowed = 'move';
    event.target.classList.add('is-dragging');
  }

  function handleDragEnd(event) {
    event.target.classList.remove('is-dragging');
  }

  function saveEdit() {
    if (editedTitle.trim() && onEditTask) {
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
    if (onDeleteTask) {
      onDeleteTask(task.id);
    }
  }
</script>

<TaskModal 
  {task} 
  show={showModal} 
  on:close={() => showModal = false}
  on:save={handleTaskUpdate}
/>

<li
  class="task {isDragging ? 'is-dragging' : ''}"
  draggable="true"
  on:dragstart={handleDragStart}
  on:dragend={handleDragEnd}
  on:click={() => showModal = true}
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
      <button class="details-button" on:click={() => showModal = true}>Details</button>
      <button 
        class="delete-button"
        on:click={handleDelete}
        title="Delete task"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke-width="1.5" 
          stroke="currentColor" 
          class="delete-icon"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            d="M15 12H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" 
          />
        </svg>
      </button>
    </div>
  {/if}
</li>

<style>
  .task {
    background-color: #ffffff;
    padding: 14px 16px;
    margin-bottom: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(9, 30, 66, 0.1);
    cursor: grab;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid #e1e4e8;
    user-select: none;
    min-height: 48px;
    position: relative;
    overflow: hidden;
  }

  .task:hover {
    background-color: #f8fafc;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(9, 30, 66, 0.15);
    border-color: #d0d7de;
  }

  .task.is-dragging {
    opacity: 0.95;
    transform: scale(1.02) rotate(0.5deg);
    box-shadow: 0 8px 16px rgba(9, 30, 66, 0.3);
    background: #ffffff;
    cursor: grabbing;
    border: 1px solid #4c9aff;
  }

  input {
    flex: 1;
    margin-right: 8px;
    padding: 8px 12px;
    border: 2px solid #4c9aff;
    border-radius: 6px;
    font-size: 14px;
    background: white;
    box-shadow: 0 0 0 3px rgba(76, 154, 255, 0.15);
    transition: all 0.2s ease;
  }

  input:focus {
    outline: none;
    box-shadow: 0 0 0 4px rgba(76, 154, 255, 0.2);
  }

  span {
    font-size: 14px;
    color: #1f2937;
    flex: 1;
    padding: 4px 6px;
    line-height: 1.4;
    font-weight: 500;
  }

  .task-actions {
    display: flex;
    gap: 8px;
    align-items: center;
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  .task:hover .task-actions {
    opacity: 1;
  }

  .details-button {
    padding: 6px 12px;
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    color: #374151;
    font-weight: 500;
    font-size: 12px;
    border-radius: 6px;
    transition: all 0.2s ease;
  }

  .details-button:hover {
    background: #e5e7eb;
    color: #111827;
    border-color: #9ca3af;
  }

  .delete-button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
    border-radius: 6px;
    background: #fee2e2;
    border: 1px solid #fecaca;
    color: #ef4444;
    transition: all 0.2s ease;
  }

  .delete-button:hover {
    background: #fecaca;
    color: #dc2626;
    transform: scale(1.05);
  }

  .delete-icon {
    width: 18px;
    height: 18px;
    transition: all 0.2s ease;
  }

  /* Modal styles enhancement */
  .modal-backdrop {
    backdrop-filter: blur(2px);
    background: rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
  }

  .modal {
    background: white;
    padding: 24px;
    border-radius: 12px;
    min-width: 400px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }
</style>
