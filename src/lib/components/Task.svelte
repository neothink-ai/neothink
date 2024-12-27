<script>
  export let task;
  export let onEditTask;
  export let onDeleteTask;

  let isEditing = false;
  let editedTitle = task.title;
  let isDragging = false;

  function handleDragStart(event) {
    isDragging = true;
    event.dataTransfer.setData('taskId', task.id);
    event.dataTransfer.effectAllowed = 'move';
  }

  function handleDragEnd() {
    isDragging = false;
  }

  function saveEdit() {
    if (editedTitle.trim()) {
      onEditTask(task.id, editedTitle);
      isEditing = false;
    }
  }

  function cancelEdit() {
    editedTitle = task.title;
    isEditing = false;
  }

  function handleDelete(event) {
    event.stopPropagation(); // Prevent event bubbling
    onDeleteTask(task.id);
  }
</script>

<li
  class="task {isDragging ? 'is-dragging' : ''}"
  draggable="true"
  on:dragstart={handleDragStart}
  on:dragend={handleDragEnd}
  data-task-id={task.id}
>
  {#if isEditing}
    <input 
      bind:value={editedTitle} 
      on:blur={saveEdit} 
      on:keyup="{e => e.key === 'Enter' && saveEdit()}"
    />
    <button on:click|stopPropagation={cancelEdit}>Cancel</button>
  {:else}
    <span on:dblclick|stopPropagation={() => isEditing = true}>{task.title}</span>
    <button 
      class="delete-button"
      on:click|stopPropagation={handleDelete}
    >
      Delete
    </button>
  {/if}
</li>

<style>
  .task {
    background-color: #fff;
    padding: 12px;
    margin-bottom: 8px;
    border-radius: 3px;
    box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25);
    cursor: grab;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 
      background-color 0.2s ease,
      transform 0.1s ease,
      box-shadow 0.1s ease;
    border: 2px solid transparent;
    user-select: none;
    transform-origin: center;
  }
  .task:hover {
    background-color: #f4f5f7;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(9, 30, 66, 0.15);
  }
  .task.is-dragging {
    opacity: 0.9;
    transform: scale(1.02);
    box-shadow: 0 8px 16px rgba(9, 30, 66, 0.25);
    background: #fff;
    cursor: grabbing;
  }
  .task:active {
    cursor: grabbing;
    transform: scale(1.02);
  }
  input {
    flex: 1;
    margin-right: 8px;
    padding: 6px 8px;
    border: 2px solid #4c9aff;
    border-radius: 3px;
    font-size: 14px;
    background: white;
    box-shadow: 0 0 0 2px rgba(76, 154, 255, 0.2);
  }
  input:focus {
    outline: none;
  }
  button {
    padding: 4px 8px;
    background: transparent;
    border: none;
    color: #42526e;
    cursor: pointer;
    border-radius: 3px;
    font-size: 12px;
    transition: all 0.15s ease;
  }
  button:hover {
    color: #FF5630;
    background: rgba(255, 86, 48, 0.08);
  }
  span {
    font-size: 14px;
    color: #172b4d;
    flex: 1;
    padding: 2px 4px;
  }
</style>
