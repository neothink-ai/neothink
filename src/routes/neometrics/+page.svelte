<script>
    import { user } from '$lib/stores/userStore.js';
    import Personalview from './personal/+page.svelte';
    import Teamview from './team/+page.svelte';

    let view = 'personal';
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sauce&display=swap');

    main {
        position: relative;
        transition: transform 0.3s ease;
        overflow-y: auto; /* Enable vertical scrolling */
        height: 100vh; /* Ensure it takes the full viewport height */
    }

    .welcome {
        position: fixed;
        top: 10px;
        margin-top: 20px;
        left: 350px;
        font-family: 'Open Sauce', sans-serif;
        font-weight: bold;
        font-size: 3rem;
        color: #00bf63;
    }

    .username {
        color: black;
    }

    .comma {
        color: #00bf63;
    }

    .exclamation {
        color: black;
    }

    .main-content {
        padding: 20px; /* Add padding to the main content */
    }

</style>

<main>
    <div class="welcome">
        {#if $user}
            Welcome<span class="comma">,</span> <span class="username">{$user?.displayName}</span><span class="exclamation">!</span>
        {/if}
    </div>
    <div class="main-content">
        {#if view === 'personal'}
            <Personalview />
        {:else if view === 'team'}
            <Teamview />
        {/if}
    </div>
</main>
