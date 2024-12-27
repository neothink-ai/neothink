<script>
  import Column from '$lib/components/Column.svelte';
  import { onMount } from 'svelte';

  export let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  export let tasks = [
    { id: 'task1', title: 'First Task', columnId: 'todo' }
  ];

  let isDragging = false;

  function handleDragStart() {
    isDragging = true;
  }

  function handleDragEnd() {
    isDragging = false;
  }

  function addTask(title, columnId) {
    const newTask = {
      id: `task${tasks.length + 1}`,
      title,
      columnId
    };
    tasks = [...tasks, newTask];
    saveTasks();
  }

  function moveTask(taskId, newColumnId, targetIndex) {
    const taskToMove = tasks.find(t => t.id === taskId);
    if (!taskToMove) return;

    const updatedTasks = tasks.filter(t => t.id !== taskId);
    const targetColumnTasks = updatedTasks.filter(t => t.columnId === newColumnId);
    
    // Calculate the actual index in the full tasks array
    let insertAtIndex;
    if (targetIndex === 0) {
      // Insert at the beginning of the column
      insertAtIndex = updatedTasks.findIndex(t => t.columnId === newColumnId);
      if (insertAtIndex === -1) insertAtIndex = updatedTasks.length;
    } else if (targetIndex >= targetColumnTasks.length) {
      // Insert at the end of the column
      const lastColumnTask = [...targetColumnTasks].pop();
      insertAtIndex = lastColumnTask 
        ? updatedTasks.indexOf(lastColumnTask) + 1 
        : updatedTasks.length;
    } else {
      // Insert at specific position
      const targetTask = targetColumnTasks[targetIndex];
      insertAtIndex = updatedTasks.indexOf(targetTask);
    }

    // Insert the task at the calculated position
    updatedTasks.splice(insertAtIndex, 0, { ...taskToMove, columnId: newColumnId });
    tasks = updatedTasks;
    saveTasks();
  }

  function editTask(taskId, newTitle) {
    tasks = tasks.map(task =>
      task.id === taskId ? { ...task, title: newTitle } : task
    );
    saveTasks();
  }

  function deleteTask(taskId) {
    tasks = tasks.filter(task => task.id !== taskId);
    saveTasks();
  }

  function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }

  function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
      tasks = JSON.parse(savedTasks);
    }
  }

  onMount(() => {
    loadTasks();
  });
</script>

<div 
  class="kanban-board {isDragging ? 'dragging' : ''}" 
  on:dragstart={handleDragStart} 
  on:dragend={handleDragEnd}
>
  {#each columns as column}
    <Column
      {column}
      {tasks}
      on:addTask={(event) => addTask(event.detail.title, column.id)}
      on:moveTask={(event) => moveTask(
        event.detail.taskId, 
        column.id, 
        event.detail.targetIndex
      )}
      on:editTask={(event) => editTask(event.detail.taskId, event.detail.newTitle)}
      on:deleteTask={(event) => deleteTask(event.detail.taskId)}
    />
  {/each}
</div>

<style>
  .kanban-board {
    display: flex;
    gap: 12px;
    padding: 24px;
    overflow-x: auto;
    height: calc(100vh - 48px);
    background-color: #f4f5f7;
    transition: background-color 0.2s ease;
    align-items: flex-start;
  }
  .kanban-board.dragging {
    background-color: #ebecf0;
  }
</style>
