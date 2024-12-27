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
      dispatch('addTask', { title: newTaskTitle });
      newTaskTitle = '';
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
  }

  function handleDrop(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData('taskId');
    dispatch('moveTask', { taskId });
  }
</script>

<div
  class="column"
  on:drop={handleDrop}
  role="list"
>
>
  <h2>{column.title}</h2>
  <div class="task-input">
    <input
      placeholder="New task"
      bind:value={newTaskTitle}
      on:keyup={(e) => e.key === 'Enter' && handleAddTask()}
    />
    <button on:click={handleAddTask}>Add</button>
  </div>
  <ul>
    {#each tasks.filter(task => task.columnId === column.id) as task}
      <Task {task} />
    {/each}
  </ul>
</div>

<style>
  .column {
    flex: 1;
    border: 1px solid #ccc;
    padding: 8px;
    border-radius: 4px;
    background-color: #f9f9f9;
  }
  .task-input {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
  }
  input {
    flex: 1;
    padding: 4px;
  }
  button {
    padding: 4px 8px;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
</style>
