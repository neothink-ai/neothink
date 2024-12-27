<script>
  import Task from '$lib/components/Task.svelte';
  import { createEventDispatcher } from 'svelte';
  import { slide } from 'svelte/transition';

  export let column;
  /** @type {Array<{ id: string, columnId: string, title: string }>} */
  export let tasks = [];

  const dispatch = createEventDispatcher();
  let newTaskTitle = '';
  let isAddingTask = false;
  let dragOverIndex = -1;
  let dropTarget = null;
  let isAddingTaskAtBottom = false;
  let bottomInputRef;

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
    
    // Throttle the drag over calculations
    if (dropTarget && dropTarget === event.target) {
      return;
    }
    dropTarget = event.target;
    
    let newDragOverIndex = -1;
    
    for (let i = 0; i < taskElements.length; i++) {
      const rect = taskElements[i].getBoundingClientRect();
      const threshold = rect.top + (rect.height * 0.5);
      
      if (mouseY < threshold) {
        newDragOverIndex = i;
        break;
      }
    }
    
    if (newDragOverIndex === -1) {
      newDragOverIndex = columnTasks.length;
    }
    
    dragOverIndex = newDragOverIndex;
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

  function handleAddTaskFromBottom() {
    if (newTaskTitle.trim()) {
      dispatch('addTask', { title: newTaskTitle, columnId: column.id });
      newTaskTitle = '';
      isAddingTaskAtBottom = false;
    }
  }

  $: if (isAddingTaskAtBottom) {
    setTimeout(() => bottomInputRef?.focus(), 0);
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
  
  <div class="create-task-bottom">
    {#if isAddingTaskAtBottom}
      <div class="bottom-input-container" transition:slide|local>
        <input
          bind:this={bottomInputRef}
          bind:value={newTaskTitle}
          placeholder="Enter task title..."
          on:keyup="{e => e.key === 'Enter' && handleAddTaskFromBottom()}"
          on:blur={() => {
            if (!newTaskTitle.trim()) isAddingTaskAtBottom = false;
          }}
        />
        <div class="bottom-input-actions">
          <button class="add-button" on:click={handleAddTaskFromBottom}>Add</button>
          <button 
            class="cancel-button"
            on:click={() => {
              isAddingTaskAtBottom = false;
              newTaskTitle = '';
            }}
          >Cancel</button>
        </div>
      </div>
    {:else}
      <button 
        class="create-button" 
        on:click={() => isAddingTaskAtBottom = true}
      >
        <span class="plus">+</span> Create
      </button>
    {/if}
  </div>
</div>

<style>
  .column {
    flex: 0 0 280px;
    border-radius: 8px;
    background-color: #ebecf0;
    padding: 12px;
    max-height: 100%;
    overflow-y: auto;
    transition: background-color 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 0;
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
    padding: 1px 0;
    margin: 0;
    min-height: 40px;
    flex: 1;
    overflow-y: auto;
    margin-bottom: 0;
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
    margin: 0;
    border-radius: 1px;
    pointer-events: none;
    transition: all 0.2s ease;
    animation: scaleIn 0.15s ease-out;
  }

  @keyframes scaleIn {
    from {
      transform: scaleY(0);
    }
    to {
      transform: scaleY(1);
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .create-task-bottom {
    margin-top: 8px;
    display: flex;
    justify-content: flex-end;
  }

  .create-button {
    padding: 4px 8px;
    background: transparent;
    border: none;
    border-radius: 3px;
    color: #42526E;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 4px;
    opacity: 0.8;
  }

  .create-button:hover {
    background: rgba(9, 30, 66, 0.04);
    color: #172B4D;
    opacity: 1;
  }

  .plus {
    font-size: 14px;
    font-weight: 500;
  }

  .bottom-input-container {
    width: 100%;
    background: white;
    border-radius: 3px;
    padding: 8px;
    box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25);
    margin-top: 4px;
  }

  .bottom-input-actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }

  .bottom-input-actions button {
    flex: 1;
    padding: 6px 12px;
    border: none;
    border-radius: 3px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .add-button {
    background: #36B37E;
    color: white;
  }

  .add-button:hover {
    background: #2ea06e;
  }
</style>
