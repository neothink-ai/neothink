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
    padding: 8px;
    margin-bottom: 8px;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    cursor: grab;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .task:active {
    cursor: grabbing;
  }
  input {
    flex: 1;
    margin-right: 8px;
    padding: 4px;
  }
  button {
    background: none;
    border: none;
    color: #ff4d4f;
    cursor: pointer;
  }
</style>
