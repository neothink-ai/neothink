<script>
    import { user } from '$lib/stores/userStore.js';
    import Sidebar from '../neometrics/components/Sidebar.svelte';
    import ProfileMenu from '$lib/components/ProfileMenu.svelte';
    import { writable } from 'svelte/store';
    import Personalview from './Personalview.svelte';
    import Teamview from './Teamview.svelte';

    let sidebarOpen = writable(false);
    let currentView = writable('personal');

    function toggleSidebar() {
        sidebarOpen.update(open => !open);
    }

    function setView(view) {
        currentView.set(view);
    }
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sauce&display=swap');

    main {
        position: relative;
        transition: transform 0.3s ease;
    }

    .logo {
        position: fixed;
        top: 10px;
        left: 10px;
        max-width: 250px;
        margin-top: 30px;
        height: auto;
        margin-left: 40px;
    }

    .view-buttons {
        position: fixed;
        margin-top: 40px;
        margin-left: 25px;
        top: 80px;
        left: 10px;
        display: flex;
        gap: 10px;
    }

    .view-button {
        font-family: 'Open Sauce', sans-serif;
        font-size: 1rem;
        font-weight: bold;
        color: black;
        background-color: white;
        border: 2px solid #00bf63;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    .view-button.selected {
        background-color: #00bf63;
        color: white;
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

    .sidebar-open {
        transform: translateX(250px);
    }

    .profile-menu {
        position: fixed;
        top: 10px;
        right: 10px;
    }
</style>

<main class:sidebar-open={$sidebarOpen}>
    <Sidebar {sidebarOpen} />
    <div class="welcome">
        {#if $user}
            Welcome<span class="comma">,</span> <span class="username">{$user?.displayName}</span><span class="exclamation">!</span>
        {/if}
    </div>
    <img class="logo" src="/assets/neometrics1.png" alt="Neometrics Logo">
    <div class="view-buttons">
        <button class="view-button" class:selected={$currentView === 'personal'} on:click={() => setView('personal')}>Personal View</button>
        <button class="view-button" class:selected={$currentView === 'team'} on:click={() => setView('team')}>Team View</button>
    </div>
    <div class="main-content">
        {#if $currentView === 'personal'}
            <Personalview />
        {:else if $currentView === 'team'}
            <Teamview />
        {/if}
    </div>
    <div class="profile-menu">
        <ProfileMenu />
    </div>
</main>
