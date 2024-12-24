<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/userStore';
  import Sidebar from './home/components/Sidebar.svelte';
  import TopBar from '$lib/components/TopBar.svelte';
  
  onMount(() => {
    const unsubscribe = user.subscribe((currentUser) => {
      if (currentUser && (window.location.pathname === '/landing-page' || window.location.pathname === '/sign-up')) {
        goto('/home');
      } else if (!currentUser && window.location.pathname.startsWith('/home')) {
        goto('/landing-page');
      }
    });
    
    return () => {
      unsubscribe();
    };
  });

  $: showSidebar = $user && !['/landing-page', '/sign-up'].includes(window.location.pathname);
</script>

<div class="min-h-screen bg-gray-100">
  {#if showSidebar}
    <TopBar />
    <div class="flex">
      <Sidebar />
      <main class="flex-1">
        <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
    </div>
  {:else}
    <slot />
  {/if}
</div>