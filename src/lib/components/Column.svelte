<script>
  import Task from '$lib/components/Task.svelte';
  import { createEventDispatcher } from 'svelte';

  export let column;
  /** @type {Array<{ id: string, columnId: string, title: string }>} */
  export let tasks = [];

  const dispatch = createEventDispatcher();
  let newTaskTitle = '';
  let isAddingTask = false;
  let dragOverIndex = -1;

  function handleAddTask() {
    if (newTaskTitle.trim()) {
      dispatch('addTask', { title: newTaskTitle, columnId: column.id });
      newTaskTitle = '';
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
    const columnTasks = tasks.filter(task => task.columnId === column.id);
    const taskElements = Array.from(event.currentTarget.querySelectorAll('.task'));
    const mouseY = event.clientY;
    
    let newDragOverIndex = -1;
    
    // Find the insertion point
    for (let i = 0; i < taskElements.length; i++) {
      const rect = taskElements[i].getBoundingClientRect();
      const middleY = rect.top + rect.height / 2;
      
      if (mouseY < middleY) {
        newDragOverIndex = i;
        break;
      }
    }
    
    // If we're below all tasks, set index to the end
    if (newDragOverIndex === -1) {
      newDragOverIndex = columnTasks.length;
    }
    
    if (dragOverIndex !== newDragOverIndex) {
      dragOverIndex = newDragOverIndex;
    }
  }

  function handleDrop(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData('taskId');
    const currentTask = tasks.find(t => t.id === taskId);
    
    // Only dispatch if we're actually moving the task
    if (currentTask && (currentTask.columnId !== column.id || dragOverIndex !== -1)) {
      dispatch('moveTask', { 
        taskId, 
        newColumnId: column.id,
        targetIndex: dragOverIndex
      });
    }
    
    dragOverIndex = -1;
  }

  function handleEditTask(taskId, newTitle) {
    dispatch('editTask', { taskId, newTitle });
  }

  function handleDeleteTask(taskId) {
    dispatch('deleteTask', { taskId });
  }

  $: taskCount = tasks.filter(task => task.columnId === column.id).length;
</script>

<div
  class="column"
  on:drop={handleDrop}
  on:dragover={handleDragOver}
  on:dragleave={() => dragOverIndex = -1}
  role="list"
>
  <div class="column-header">
    <div class="header-title">
      <h2>{column.title}</h2>
      <span class="task-count">{taskCount}</span>
    </div>
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
    {#each tasks.filter(task => task.columnId === column.id) as task, index}
      {#if dragOverIndex === index}
        <div class="drop-indicator" />
      {/if}
      <Task
        {task}
        onEditTask={handleEditTask}
        onDeleteTask={handleDeleteTask}
      />
    {/each}
    {#if dragOverIndex === tasks.filter(task => task.columnId === column.id).length}
      <div class="drop-indicator" />
    {/if}
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
    margin-bottom: 0;
    padding: 0 4px;
  }
  .column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
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
    padding: 4px 8px;
    border: 1px solid transparent;
    border-radius: 3px;
    font-size: 13px;
    font-weight: 400;
    transition: all 0.15s ease;
    cursor: pointer;
    background: transparent;
  }
  .new-task-actions button:first-child {
    color: #36B37E;
  }
  .new-task-actions button:first-child:hover {
    background: rgba(54, 179, 126, 0.1);
    border-color: #36B37E;
  }
  .cancel-button {
    color: #42526E;
  }
  .cancel-button:hover {
    background: rgba(255, 86, 48, 0.1);
    border-color: #FF5630;
    color: #FF5630;
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
  .header-title {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .task-count {
    font-size: 12px;
    color: #5E6C84;
    background: rgba(9, 30, 66, 0.04);
    padding: 2px 6px;
    border-radius: 10px;
    min-width: 20px;
    text-align: center;
    transition: all 0.2s ease;
  }

  .drop-indicator {
    height: 2px;
    background: #4c9aff;
    margin: 4px 0;
    border-radius: 1px;
    animation: fadeIn 0.2s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
</style>
