<script>
    import { user } from '$lib/stores/userStore.js';
    import Sidebar from '../neometrics/components/Sidebar.svelte';
    import ProfileMenu from '$lib/components/ProfileMenu.svelte';
    import { writable } from 'svelte/store';

    let sidebarOpen = writable(false);

    function toggleSidebar() {
        sidebarOpen.update(open => !open);
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
        left: 10px; /* Move to the left */
        max-width: 250px;
        margin-top: 30px;
        height: auto;
        margin-left: 40px;
    }

    .welcome {
        position: fixed;
        top: 10px;
        margin-top: 20px;
        left: 350px; /* Adjust this value to move it to the right */
        font-family: 'Open Sauce', sans-serif;
        font-weight: bold;
        font-size: 3rem;
        color: #00bf63; /* Change color to green */
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
        transform: translateX(250px); /* Adjust this value based on sidebar width */
    }

    .profile-menu {
        position: fixed; /* Change to fixed */
        top: 10px;
        right: 10px; /* Position it in the top right corner */
    }

    .analytics-overview {
        font-family: 'Open Sauce', sans-serif;
        font-size: 1.5rem;
        font-weight: bold; /* Make the text bold */
        color: black;
        margin-top: 80px; /* Adjust the margin as needed */
        text-align: left;
        margin-left: 30px;
    }
</style>

<main class:sidebar-open={$sidebarOpen}>
    <div class="welcome">
        {#if $user}
            Welcome<span class="comma">,</span> <span class="username">{$user?.displayName}</span><span class="exclamation">!</span>
        {/if}
    </div>
    <img class="logo" src="/assets/neometrics1.png" alt="Neometrics Logo">
    <div class="analytics-overview">Analytics Overview</div> <!-- Moved below the welcome message -->
    <div class="main-content">
        <Sidebar {toggleSidebar} />
    </div>
    <div class="profile-menu">
        <ProfileMenu />
    </div>
</main>
