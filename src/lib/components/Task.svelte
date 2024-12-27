<script>
  export let task;

  function handleDragStart(event) {
    event.dataTransfer.setData('taskId', task.id);
  }
</script>

<li
  class="task"
  draggable="true"
  on:dragstart={handleDragStart}
>
  {task.title}
</li>

<style>
  .task {
    background-color: #fff;
    padding: 8px;
    margin-bottom: 8px;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    cursor: grab;
  }
  .task:active {
    cursor: grabbing;
  }
</style>
