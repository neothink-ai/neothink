<script>
  import Column from '$lib/components/Column.svelte';
  import { taskStore } from '$lib/stores/taskStore';
  import { authStore } from '$lib/stores/authStore';
  import { onMount, createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition'; // Add this import

  // Declare props with default values
  export let columns = [
    { id: 'todo', title: 'To Do' },
    { id: 'inProgress', title: 'In Progress' },
    { id: 'done', title: 'Done' }
  ];

  let tasks = [];
  let loading = false;
  let error = null;
  let authError = null;

  const dispatch = createEventDispatcher();

  // Subscribe to taskStore
  taskStore.subscribe(state => {
    tasks = state.tasks || [];
    loading = state.loading;
    error = state.error;
  });

  let isDragging = false;

  function handleDragStart() {
    isDragging = true;
  }

  function handleDragEnd() {
    isDragging = false;
  }

  // Task operations
  async function addTask(event) {
    try {
      await taskStore.addTask(event.detail);
    } catch (err) {
      console.error('Failed to add task:', err);
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
      const user = $authStore.user;
      if (!user) return;

      const response = await fetch(`http://localhost:6876/tasks?userid=${user.uid}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Raw tasks data:', data);  // Debug log

      if (Array.isArray(data)) {
        const processedTasks = data.map(task => ({
          id: task._id.$oid,
          title: task.title,
          columnId: task.columnId,
          state: task.state,
          priority: task.priority,
          size: task.size,
          deadline: task.deadline,
          assignee: task.assignee,
          userid: task.userid,
          assigned_time: task.assigned_time,
          completed_time: task.completed_time,
          description: task.description
        }));
        taskStore.setTasks(processedTasks);
      }
    } catch (error) {
      console.error('Failed to load tasks:', error);
    }
  }

  onMount(async () => {
    if ($authStore.user) {
      await loadTasks();
    }
  });

  $: if ($authStore.user) {
    loadTasks();
  }

  $: isAuthenticated = $authStore.user !== null;

  async function handleAddTask(event) {
    if (!isAuthenticated) {
      authError = 'Please sign in to add tasks';
      return;
    }
    try {
      const user = $authStore.user;
      if (!user) throw new Error('Authentication required');

      await taskStore.addTask({
        title: event.detail.title,
        columnId: event.detail.columnId,
        userid: user.uid
      });
      authError = null;
    } catch (err) {
      console.error('Failed to add task:', err);
      authError = err.message;
    }
  }
</script>

<div 
  class="kanban-board {isDragging ? 'dragging' : ''}" 
  on:dragstart={handleDragStart} 
  on:dragend={handleDragEnd}
>
  {#if authError}
    <div class="auth-error" transition:fade|local>{authError}</div>
  {/if}

  {#if !isAuthenticated}
    <div class="auth-warning">
      Please sign in to manage tasks
    </div>
  {/if}

  {#if error}
    <div class="error-message">{error}</div>
  {/if}

  {#if loading}
    <div class="loading">Loading tasks...</div>
  {:else}
    {#each columns as column (column.id)}
      <Column
        {column}
        tasks={tasks.filter(task => task?.columnId === column.id) || []}
        on:addTask={handleAddTask}
        on:moveTask={moveTask}
        on:editTask={(event) => editTask(event.detail.taskId, event.detail.newTitle)}
        on:deleteTask={(event) => deleteTask(event.detail.taskId)}
      />
    {/each}
  {/if}
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

  .auth-error {
    background: #ffebe6;
    color: #de350b;
    padding: 8px 16px;
    border-radius: 3px;
    margin-bottom: 16px;
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 1000;
  }

  .auth-warning {
    background: #fffae6;
    color: #172b4d;
    padding: 8px 16px;
    border-radius: 3px;
    margin-bottom: 16px;
    text-align: center;
  }
</style>
