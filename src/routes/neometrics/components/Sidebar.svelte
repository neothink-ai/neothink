<script>
    let activeItem = 'analytics';
    let isSidebarOpen = false;

    function toggleSidebar() {
        isSidebarOpen = !isSidebarOpen;
    }
</script>

<style>
    .sidebar {
        position: fixed;
        left: 0;
        top: 0;
        height: 100%;
        width: 300px;
        background-color: #f3f4f6;
        padding: 20px;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        transform: translateX(-100%);
        z-index: 1000;
    }

    .sidebar.open {
        transform: translateX(0);
    }

    .menu-item {
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 16px;
        font-weight: bold;
        color: black;
        padding: 10px 0;
        cursor: pointer;
        transition: color 0.3s;
        text-decoration: none;
        display: block;
        position: relative;
    }

    .menu-item:hover,
    .menu-item.active {
        color: #00bf63;
    }

    .menu-item.active::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 0;
        bottom: 0;
        width: 5px;
        background-color: #00bf63;
    }

    .menu-item + .menu-item {
        margin-top: 10px;
    }

    .toggle-button {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: #f3f4f6;
        color: black;
        border: none;
        padding: 10px;
        cursor: pointer;
        z-index: 1001;
        font-weight: bold;
    }

    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        transition: opacity 0.3s;
        opacity: 0;
        pointer-events: none;
        z-index: 999;
    }

    .overlay.open {
        opacity: 1;
        pointer-events: auto;
    }

    .sidebar img {
        max-width: 100%;
        margin-top: 30px;
        margin-bottom: 50px;
    }
</style>

<div class="overlay {isSidebarOpen ? 'open' : ''}" on:click={toggleSidebar}></div>

<div class="sidebar {isSidebarOpen ? 'open' : ''}">
    <img src="/assets/neometrics.png" alt="Neometrics Logo">
    <a href="/home" class="menu-item" class:active={activeItem === 'home'} on:click={() => activeItem = 'home'}>Home Page</a>
    <button type="button" class="menu-item" class:active={activeItem === 'analytics'} on:click={() => activeItem = 'analytics'} aria-role="button">Analytics Overview</button>
    <button type="button" class="menu-item" class:active={activeItem === 'individual'} on:click={() => activeItem = 'individual'} aria-role="button">Individual Performance</button>
    <button type="button" class="menu-item" class:active={activeItem === 'team'} on:click={() => activeItem = 'team'} aria-role="button">Team Performance</button>
    <button type="button" class="menu-item" class:active={activeItem === 'project'} on:click={() => activeItem = 'project'} aria-role="button">Project Insights</button>
    <button type="button" class="menu-item" class:active={activeItem === 'ai'} on:click={() => activeItem = 'ai'} aria-role="button">AI Assistant</button>
</div>

<button class="toggle-button" on:click={toggleSidebar}>
    {isSidebarOpen ? '<' : '>'}
</button>