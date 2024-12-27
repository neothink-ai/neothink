<script>
  import KanbanBoard from '$lib/components/KanbanBoard.svelte';
  import { onMount } from 'svelte';

  let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [
    { id: 'task1', title: 'First Task', columnId: 'todo' },
    // Add more tasks as needed
  ];

  function addTask(title, columnId) {
    const newTask = {
      id: `task${tasks.length + 1}`,
      title,
      columnId
    };
    tasks = [...tasks, newTask];
    saveTasks();
  }

  function moveTask(taskId, newColumnId) {
    tasks = tasks.map(task =>
      task.id === taskId ? { ...task, columnId: newColumnId } : task
    );
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
