<script>
    import Column from '$lib/components/Column.svelte';
  
    export let columns = [
      { id: 'todo', title: 'To Do' },
      { id: 'inProgress', title: 'In Progress' },
      { id: 'done', title: 'Done' }
    ];
  
    export let tasks = [
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
    }
  
    function moveTask(taskId, newColumnId) {
      tasks = tasks.map(task =>
        task.id === taskId ? { ...task, columnId: newColumnId } : task
      );
    }
  </script>
  
  <div class="kanban-board">
    {#each columns as column}
      <Column
        {column}
        {tasks}
        on:addTask={(event) => addTask(event.detail.title, column.id)}
        on:moveTask={(event) => moveTask(event.detail.taskId, column.id)}
      />
    {/each}
  </div>
  
  <style>
    .kanban-board {
      display: flex;
      gap: 16px;
    }
  </style>
  