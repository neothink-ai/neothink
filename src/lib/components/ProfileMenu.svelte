<script>
  import { user } from '$lib/stores/userStore';
  import { logOut } from '$lib/backend/auth';
  
  let isOpen = false;
  
  function toggleMenu() {
    isOpen = !isOpen;
  }
  
  function handleClickOutside(event) {
    const menu = event.target.closest('.profile-menu');
    if (!menu) {
      isOpen = false;
    }
  }
  
  async function handleLogout() {
    try {
      await logOut();
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
</script>

<svelte:window on:click={handleClickOutside} />

<div class="profile-menu relative">
  <button
    on:click={toggleMenu}
    class="flex items-center space-x-2 rounded-lg bg-gray-200 px-4 py-2 hover:bg-gray-300 transition-colors"
  >
    <span class="text-gray-700">
      {#if $user}
        {$user.displayName}
      {:else}
        Loading...
      {/if}
    </span>
    <span class="text-xl">👤</span>
  </button>
  
  {#if isOpen}
    <div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2">
      {#if $user}
        <div class="px-4 py-2 border-b border-gray-100">
          <div class="font-medium">{$user.displayName}</div>
          <div class="text-sm text-gray-500">{$user.email}</div>
        </div>
      {/if}
      <a href="/about" class="block px-4 py-2 hover:bg-gray-100">About</a>
      <a href="/settings" class="block px-4 py-2 hover:bg-gray-100">Settings</a>
      <button
        class="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600"
        on:click={handleLogout}
      >
        Logout
      </button>
    </div>
  {/if}
</div>