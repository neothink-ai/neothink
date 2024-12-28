<script>
  import KanbanBoard from '$lib/components/KanbanBoard.svelte';
  import { onMount } from 'svelte';
  import { getAuth } from 'firebase/auth'; // Import Firebase auth

  let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [];

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

  onMount(async () => {
    const auth = getAuth();
    const user = auth.currentUser;
    if (user) {
      await fetchTasks(user.uid);
    } else {
      console.error('User not logged in');
    }
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
  <KanbanBoard {columns} {tasks} on:addTask={addTask} on:moveTask={moveTask} />
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
