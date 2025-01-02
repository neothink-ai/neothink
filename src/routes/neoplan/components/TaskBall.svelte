<script>
    export let task;
    export let index;
    
    const colors = [
        '#0052CC', '#36B37E', '#FF5630', 
        '#6554C0', '#00B8D9', '#FFAB00'
    ];
    
    $: ballColor = colors[index % colors.length];
</script>

<div 
    class="task-ball" 
    style="background-color: {ballColor}"
    on:click
>
    <div class="task-content">
        <h3>{task.title}</h3>
        <p class="description">{task.description}</p>
        <div class="task-meta">
            <span class="priority {task.priority.toLowerCase()}">{task.priority}</span>
            <span class="size">{task.size}</span>
        </div>
    </div>
</div>

<style>
    .task-ball {
        width: 100%;
        aspect-ratio: 1;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }

    .task-ball:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    }

    .task-ball:active {
        transform: translateY(0) scale(0.98);
    }

    .task-content {
        padding: 24px;
        text-align: center;
        color: white;
        width: 100%;
    }

    h3 {
        margin: 0 0 8px 0;
        font-size: 16px;
        font-weight: 600;
        line-height: 1.4;
    }

    .description {
        font-size: 14px;
        opacity: 0.9;
        margin: 0 0 16px 0;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .task-meta {
        display: flex;
        gap: 8px;
        justify-content: center;
        font-size: 12px;
    }

    .priority, .size {
        padding: 2px 8px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(4px);
    }
</style>
