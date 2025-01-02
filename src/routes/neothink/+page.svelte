<script>
    import KanbanBoard from '$lib/components/KanbanBoard.svelte';
    import TaskGenerator from './components/TaskGenerator.svelte';
    import { user } from '$lib/stores/userStore';
</script>

<div class="page-container">
    {#if $user}
        <TaskGenerator />
        <div class="board-container">
            <KanbanBoard />
        </div>
    {:else}
        <div class="login-prompt">
            Please log in to view your tasks.
        </div>
    {/if}
</div>

<style>
    .page-container {
        padding: 20px;
        height: 100vh;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .board-container {
        flex: 1;
        min-height: 0;
    }

    .login-prompt {
        text-align: center;
        padding: 40px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
