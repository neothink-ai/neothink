<script>
  import KanbanBoard from '$lib/components/KanbanBoard.svelte';
  import { onMount } from 'svelte';
  import { user, isLoading } from '$lib/stores/userStore';
  import { goto } from '$app/navigation';
  import { taskStore } from '$lib/stores/taskStore';

  let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [];

  // Subscribe to taskStore
  taskStore.subscribe(value => {
    tasks = value.tasks || [];
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
      const newTask = {
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
      await taskStore.addTask(newTask);
      tasks = [...tasks, newTask]; // Update tasks array
    } catch (error) {
      console.error('Failed to add task:', error);
    }
  }

  async function handleMoveTask(event) {
    // Pass to KanbanBoard component
  }

  onMount(() => {
    // Redirect if not authenticated
    const unsubscribe = user.subscribe((userData) => {
      if (!$isLoading && !userData) {
        goto('/login?redirect=/kanban');
      }
    });

    return () => unsubscribe();
  });
</script>

{#if $isLoading}
  <div class="loading">Loading...</div>
{:else if $user}
  <div class="kanban-page">
    <div class="logo-container">
      <img 
        src="src\lib\assets\neotaskmaster-logo.png" 
        alt="NeoTaskMaster"
        class="logo"
      />
    </div>
    <KanbanBoard {columns} {tasks} />
  </div>
{/if}

<style>
  .kanban-page {
    height: calc(100vh - 64px); /* Account for TopBar height */
    width: 100%;
    overflow: hidden;
    position: relative;
    padding-left: 1rem; /* Add some padding from the sidebar */
  }

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
