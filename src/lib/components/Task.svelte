<script>
  export let task;
  export let onEditTask;
  export let onDeleteTask;

  let isEditing = false;
  let editedTitle = task.title;

  function handleDragStart(event) {
    event.dataTransfer.setData('taskId', task.id);
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
</script>

<li
  class="task"
  draggable="true"
  on:dragstart={handleDragStart}
>
  {#if isEditing}
    <input bind:value={editedTitle} on:blur={saveEdit} on:keyup="{e => e.key === 'Enter' && saveEdit()}" />
    <button on:click={cancelEdit}>Cancel</button>
  {:else}
    <span on:dblclick={() => isEditing = true}>{task.title}</span>
    <button on:click={() => onDeleteTask(task.id)}>Delete</button>
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
    transition: background-color 0.2s ease, transform 0.2s ease;
    border: 2px solid transparent;
  }
  .task:hover {
    background-color: #f4f5f7;
  }
  .task:active {
    cursor: grabbing;
    transform: rotate(2deg);
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
    background: none;
    border: none;
    color: #42526e;
    cursor: pointer;
    border-radius: 3px;
    font-size: 12px;
  }
  button:hover {
    background: #ebecf0;
    color: #172b4d;
  }
  span {
    font-size: 14px;
    color: #172b4d;
    flex: 1;
    padding: 2px 4px;
  }
</style>
