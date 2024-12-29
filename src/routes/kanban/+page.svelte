<script>
  import KanbanBoard from '$lib/components/KanbanBoard.svelte';
  import { onMount } from 'svelte';
  import { getAuth } from 'firebase/auth';
  import { taskStore } from '$lib/stores/taskStore';
  import { authStore } from '$lib/stores/authStore';
  import { goto } from '$app/navigation';

  let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [];

  // Subscribe to taskStore
  taskStore.subscribe(value => {
    tasks = value;
  });

  async function fetchTasks(userid) {
    try {
      const response = await fetch(`http://localhost:6876/tasks?userid=${userid}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      tasks = data;
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    }
  }

  // Task event handlers
  async function handleAddTask(event) {
    const { title, columnId } = event.detail;
    try {
      await taskStore.addTask({
        title,
        columnId,
        state: columnId,
        priority: 'Medium',
        size: 'Medium',
        deadline: null,
        assignee: null,
        assigned_time: new Date().toISOString(),
        completed_time: null
      });
    } catch (error) {
      console.error('Failed to add task:', error);
    }
  }

  async function handleMoveTask(event) {
    // Pass to KanbanBoard component
  }

  onMount(async () => {
    if ($authStore.loading) return;
    
    if (!$authStore.user) {
      goto('/login?redirect=/kanban');
      return;
    }

    await fetchTasks($authStore.user.uid);
  });
</script>

<div class="kanban-container">
  <div class="logo-container">
    <img 
      src="src\lib\assets\neotaskmaster-logo.png" 
      alt="NeoTaskMaster"
      class="logo"
    />
  </div>
  <KanbanBoard 
    {columns} 
    {tasks} 
    on:addTask={handleAddTask} 
    on:moveTask={handleMoveTask} 
  />
</div>

<style>
  .kanban-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .logo-container {
    padding: 16px 24px;
    background: #f4f5f7;
    box-shadow: 0 1px 0 rgba(9, 30, 66, 0.08);
  }

  .logo {
    height: 32px;
    width: auto;
    opacity: 0.95;
    transition: opacity 0.2s ease;
  }

  .logo:hover {
    opacity: 1;
  }
</style>
