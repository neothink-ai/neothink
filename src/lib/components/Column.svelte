<script>
  import Task from '$lib/components/Task.svelte';
  import { createEventDispatcher } from 'svelte';

  export let column;
  /** @type {Array<{ id: string, columnId: string, title: string }>} */
  export let tasks = [];

  const dispatch = createEventDispatcher();
  let newTaskTitle = '';
  let isAddingTask = false;

  function handleAddTask() {
    if (newTaskTitle.trim()) {
      dispatch('addTask', { title: newTaskTitle, columnId: column.id });
      newTaskTitle = '';
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
  }

  function handleDrop(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData('taskId');
    dispatch('moveTask', { taskId, newColumnId: column.id });
  }

  function handleEditTask(taskId, newTitle) {
    dispatch('editTask', { taskId, newTitle });
  }

  function handleDeleteTask(taskId) {
    dispatch('deleteTask', { taskId });
  }
</script>

<div
  class="column"
  on:drop={handleDrop}
  on:dragover={handleDragOver}
  role="list"
>
  <div class="column-header">
    <h2>{column.title}</h2>
    <div class="add-task-trigger">
      <span 
        class="plus-icon" 
        on:click={() => isAddingTask = !isAddingTask}
      >+</span>
    </div>
  </div>
  <ul>
    {#if isAddingTask}
      <li class="new-task-input">
        <input
          placeholder="What needs to be done?"
          bind:value={newTaskTitle}
          on:keyup="{e => e.key === 'Enter' && handleAddTask()}"
          autofocus
        />
        <div class="new-task-actions">
          <button on:click={handleAddTask}>Add</button>
          <button 
            class="cancel-button" 
            on:click={() => {
              isAddingTask = false;
              newTaskTitle = '';
            }}
          >Cancel</button>
        </div>
      </li>
    {/if}
    {#each tasks.filter(task => task.columnId === column.id) as task}
      <Task
        {task}
        onEditTask={handleEditTask}
        onDeleteTask={handleDeleteTask}
      />
    {/each}
  </ul>
</div>

<style>
  .column {
    flex: 0 0 280px;
    border-radius: 8px;
    background-color: #ebecf0;
    padding: 12px;
    max-height: 100%;
    overflow-y: auto;
  }
  h2 {
    font-size: 14px;
    font-weight: 600;
    color: #172b4d;
    margin-bottom: 12px;
    padding: 0 4px;
  }
  .column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .add-task-trigger {
    position: relative;
    cursor: pointer;
  }
  .plus-icon {
    font-size: 18px;
    color: #42526e;
    padding: 4px 8px;
    border-radius: 3px;
    transition: all 0.2s ease;
    opacity: 0.6;
    cursor: pointer;
  }
  .plus-icon:hover {
    background-color: rgba(9, 30, 66, 0.08);
    opacity: 1;
  }
  .new-task-input {
    background-color: #fff;
    padding: 8px;
    margin-bottom: 8px;
    border-radius: 3px;
    box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25);
    animation: slideIn 0.2s ease-out;
    border: 2px solid #4c9aff;
  }
  .new-task-actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }
  .new-task-actions button {
    flex: 1;
    padding: 6px 12px;
    border: none;
    border-radius: 3px;
    font-weight: 500;
    font-size: 13px;
    transition: all 0.2s ease;
    cursor: pointer;
  }
  .new-task-actions button:first-child {
    background: #36B37E;
    color: white;
  }
  .new-task-actions button:first-child:hover {
    background: #2ea06e;
    box-shadow: 0 2px 4px rgba(54, 179, 126, 0.25);
  }
  .cancel-button {
    background: #ebecf0;
    color: #42526e;
  }
  .cancel-button:hover {
    background: #ff5630;
    color: white;
    box-shadow: 0 2px 4px rgba(255, 86, 48, 0.25);
  }
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  input {
    width: 100%;
    padding: 4px 0;
    border: none;
    background: transparent;
    font-size: 14px;
    color: #172b4d;
  }
  input:focus {
    border: none;
    box-shadow: none;
    outline: none;
  }
  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    min-height: 40px;
  }
</style>
