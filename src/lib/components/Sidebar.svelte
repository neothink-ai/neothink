<script>
  export let appType = 'neoplan'; // Default value

  let activeItem = 'home';
  let isSidebarOpen = false;

  function toggleSidebar() {
    isSidebarOpen = !isSidebarOpen;
  }

  let accentColor;

  $: {
    if (appType === 'neoplan') {
      accentColor = 'bg-yellow-500';
    } else if (appType === 'neotaskmaster') {
      accentColor = 'bg-red-500';
    } else if (appType === 'neometrics') {
      accentColor = 'bg-green-500';
    } else {
      accentColor = 'bg-gray-800'; // Default color
    }
  }
</script>

<div class="overlay {isSidebarOpen ? 'open' : ''}" on:click={toggleSidebar}></div>

<div class="sidebar {isSidebarOpen ? 'open' : 'collapsed'} {accentColor}">
  <img src="/assets/neothink.png" alt="App Logo" class="logo">
  <button type="button" class="menu-item" class:active={activeItem === 'neothink'} on:click={() => activeItem = 'neothink'} aria-role="button">
    <img src="/assets/neothink_cropped.png" alt="Neothink Icon" class="icon" />
    <span>Neothink</span>
  </button>
  <div class="menu-center">
    <button type="button" class="menu-item" class:active={activeItem === 'neometrics'} on:click={() => activeItem = 'neometrics'} aria-role="button">
      <img src="/assets/neometrics_cropped.png" alt="Neometrics Icon" class="icon" />
      <span>Neometrics</span>
    </button>
    <button type="button" class="menu-item" class:active={activeItem === 'neoplan'} on:click={() => activeItem = 'neoplan'} aria-role="button">
      <img src="/assets/neoplan_cropped.png" alt="Neoplan Icon" class="icon" />
      <span>Neoplan</span>
    </button>
    <button type="button" class="menu-item" class:active={activeItem === 'neotaskmaster'} on:click={() => activeItem = 'neotaskmaster'} aria-role="button">
      <img src="/assets/neotaskmaster_cropped.png" alt="Neotaskmaster Icon" class="icon" />
      <span>Neotaskmaster</span>
    </button>
  </div>
</div>

<button class="toggle-button" on:click={toggleSidebar}>
  {isSidebarOpen ? '<' : '>'}
</button>

<style>
  .bg-yellow-500 {
    background-color: #f59e0b;
  }
  .bg-red-500 {
    background-color: #ef4444;
  }
  .bg-green-500 {
    background-color: #10b981;
  }
  .bg-gray-800 {
    background-color: #1f2937;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    width: 300px;
    background-color: #f3f4f6;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;
    transform: translateX(-100%);
    z-index: 1000;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .sidebar.collapsed {
    width: 80px;
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
    display: flex;
    align-items: center;
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

  .sidebar img.logo {
    max-width: 100%;
    margin-top: 30px;
    margin-bottom: 50px;
  }

  .icon {
    width: 34px;
    height: 34px;
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