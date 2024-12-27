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

<KanbanBoard {columns} {tasks} on:addTask={addTask} on:moveTask={moveTask} />
