<script>
  import Column from '$lib/components/Column.svelte';
  import { onMount } from 'svelte';

  export let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [];  // Initialize empty tasks array
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

  async function moveTask(event) {
    const { taskId, newColumnId, taskData } = event.detail;
    
    try {
      // Optimistically update UI
      tasks = tasks.map(t => 
        t.id === taskId ? { ...t, columnId: newColumnId } : t
      );

      const response = await fetch(`http://localhost:6876/tasks/${taskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...taskData,
          columnId: newColumnId
        })
      });

      if (!response.ok) {
        // Revert on failure
        tasks = tasks.map(t => 
          t.id === taskId ? { ...t, columnId: taskData.columnId } : t
        );
        throw new Error(`Failed to update task: ${response.statusText}`);
      }

      // Refresh tasks to ensure consistency
      await loadTasks();
    } catch (error) {
      console.error('Move task error:', error);
    }
  }

  function editTask(taskId, newTitle) {
    tasks = tasks.map(task =>
      task.id === taskId ? { ...task, title: newTitle } : task
    );
    saveTasks();
  }

  async function deleteTask(taskId) {
    try {
      const response = await fetch(`http://localhost:6876/tasks/${taskId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // Remove from local state
      tasks = tasks.filter(task => task.id !== taskId);
      
      console.log('Task deleted successfully');
      
      // Refresh tasks from server
      await loadTasks();
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  }

  async function loadTasks() {
    try {
      const response = await fetch('http://localhost:6876/tasks');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Raw tasks data:', data);  // Debug log

      if (Array.isArray(data)) {
        tasks = data.map(task => ({
          id: task._id.$oid,  // MongoDB ID
          title: task.title,
          columnId: task.columnId,
          state: task.state,
          priority: task.priority,
          size: task.size,
          deadline: task.deadline,
          assignee: task.assignee,
          assigned_time: task.assigned_time,
          completed_time: task.completed_time
        }));
        console.log('Processed tasks:', tasks);  // Debug log
      }
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
      tasks={tasks.filter(task => task.columnId === column.id)}
      on:addTask={(event) => addTask(event.detail.title, column.id)}
      on:moveTask={moveTask}
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
