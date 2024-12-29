<script>
  import { fade } from 'svelte/transition';

  export let appType = 'neoplan'; // Default value

  let activeItem = 'home';
  let isSidebarOpen = false;

  function toggleSidebar() {
    isSidebarOpen = !isSidebarOpen;
  }
</script>

<div class="overlay {isSidebarOpen ? 'open' : ''}" on:click={toggleSidebar}></div>

<div class="sidebar {isSidebarOpen ? 'open' : 'collapsed'}" on:mouseenter={() => isSidebarOpen = true} on:mouseleave={() => isSidebarOpen = false}>

  <button type="button" class="menu-item neothink" class:active={activeItem === 'neothink'} on:click={() => activeItem = 'neothink'} aria-role="button">
    <img src="/assets/neothink_cropped.png" alt="Neothink Icon" class="icon" />
    <span>Neothink</span>
  </button>
  <div class="menu-center">
    <button type="button" class="menu-item neoplan" on:click={() => { activeItem = 'neoplan'; window.location.href = '/kanban'; }} aria-role="button">
      <img src="/assets/neoplan_cropped.png" alt="Neoplan Icon" class="icon" />
      <span>Neoplan</span>
    </button>
    <button type="button" class="menu-item neotaskmaster" on:click={() => { activeItem = 'neotaskmaster'; window.location.href = '/home'; }} aria-role="button">
      <img src="/assets/neotaskmaster_cropped.png" alt="Neotaskmaster Icon" class="icon" />
      <span>Neotaskmaster</span>
    </button>
    <button type="button" class="menu-item neometrics" on:click={() => { activeItem = 'neometrics';}} aria-role="button">
      <img src="/assets/neometrics_cropped.png" alt="Neometrics Icon" class="icon" />
      <span>Neometrics</span>
    </button>
    {#if activeItem === 'neometrics'}
      <button type="button" class="menu-item personal-view" transition:fade on:click={() => window.location.href = '/neometrics/personal'}>
      <span style="margin-left: 40px;">Personal View</span>
      </button>
      <button type="button" class="menu-item team-view" transition:fade on:click={() => window.location.href = '/neometrics/team'}>
      <span style="margin-left: 40px;">Team View</span>
      </button>
    {/if}
  </div>
</div>


<style>

  .sidebar {
    position: fixed;
    left: 0;
    top: 64px; /* Adjust to match the height of the topbar */
    height: calc(100% - 64px); /* Adjust to match the height of the topbar */
    width: 80px;
    background-color: #f3f4f6;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    transition: width 0.3s;
    z-index: 1000;
  }

  .sidebar.open {
    width: 25vh;
  }

  .menu-item {
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 20px;
    font-weight: bold;
    color: black;
    padding: 10px 0;
    cursor: pointer;
    transition: color 0.3s;
    text-decoration: none;
    display: flex;
    align-items: center;
    position: relative;
  }

  .menu-item:hover,
  .menu-item.active {
    color: #00bf63;
  }
  .menu-center {
    padding-top: 25vh;
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

  .menu-item.neoplan:hover {
    color: #cbcb40;
  }

  .menu-item.neothink:hover {
    color: #7743e0;
  }
  .menu-item.neotaskmaster:hover {
    color: red;
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

  .icon {
    width: 40px;
    height: 40px;
    margin-right: 10px;
  }

  .collapsed .menu-item {
    text-align: center;
  }

  .collapsed .menu-item span {
    display: none;
  }

  .collapsed .menu-item::before {
    left: 50%;
    transform: translateX(-50%);
  }
</style>