<script>
    import KanbanBoard from '$lib/components/KanbanBoard.svelte';
  
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
    }
  
    function moveTask(taskId, newColumnId) {
      tasks = tasks.map(task =>
        task.id === taskId ? { ...task, columnId: newColumnId } : task
      );
    }
  </script>
  
  <KanbanBoard {columns} {tasks} on:addTask={addTask} on:moveTask={moveTask} />
  