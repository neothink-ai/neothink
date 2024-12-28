<script>
  import Column from '$lib/components/Column.svelte';
  import { onMount } from 'svelte';

  export let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [];
  let isDragging = false;

  function handleDragStart() {
    isDragging = true;
  }

  function handleDragEnd() {
    isDragging = false;
  }

  async function addTask(title, columnId) {
    try {
      const taskData = {
        title,
        columnId,
        state: columnId,
        priority: 'Medium',
        size: 'Medium',
        deadline: null,
        assignee: null,
        assigned_time: new Date().toISOString(),
        completed_time: null
      };

      console.log('Sending task data:', taskData); // Debug log

      const response = await fetch('http://localhost:6876/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Server error:', errorData);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await loadTasks();
    } catch (error) {
      console.error('Failed to add task:', error);
    }
  }

  async function moveTask(taskId, newColumnId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    try {
      const response = await fetch(`http://localhost:6876/tasks/${taskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: task.title,
          columnId: newColumnId,
          state: newColumnId,
          priority: task.priority || 'Medium',
          size: task.size || 'Medium',
          deadline: task.deadline || null,
          assignee: task.assignee || null,
          assigned_time: task.assigned_time,
          completed_time: newColumnId === 'done' ? new Date().toISOString() : null
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      await loadTasks();
    } catch (error) {
      console.error('Failed to move task:', error);
    }
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

  async function loadTasks() {
    try {
      const response = await fetch('http://localhost:6876/tasks');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Loaded tasks:', data); // Debug log
      tasks = data.map(task => ({
        ...task,
        id: task._id.$oid,
        columnId: task.state || task.columnId
      }));
    } catch (error) {
      console.error('Failed to load tasks:', error);
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
