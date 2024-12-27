<script>
  import Task from '$lib/components/Task.svelte';
  import { createEventDispatcher } from 'svelte';

  export let column;
  /** @type {Array<{ id: string, columnId: string, title: string }>} */
  export let tasks = [];

  const dispatch = createEventDispatcher();
  let newTaskTitle = '';

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
  <h2>{column.title}</h2>
  <div class="task-input">
    <input
      placeholder="New task"
      bind:value={newTaskTitle}
      on:keyup="{e => e.key === 'Enter' && handleAddTask()}"
    />
    <button on:click={handleAddTask}>Add</button>
  </div>
  <ul>
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
  .task-input {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
  }
  input {
    flex: 1;
    padding: 8px;
    border: 2px solid transparent;
    border-radius: 3px;
    background-color: #fff;
    box-shadow: 0 0 0 1px rgba(9, 30, 66, 0.13);
    transition: background-color 0.2s ease;
  }
  input:focus {
    border-color: #4c9aff;
    box-shadow: 0 0 0 2px rgba(76, 154, 255, 0.2);
    outline: none;
  }
  button {
    padding: 8px 12px;
    background: #0052cc;
    color: white;
    border: none;
    border-radius: 3px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  button:hover {
    background: #0065ff;
  }
  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    min-height: 40px;
  }
</style>
