<script>
  // Root layout page
  import '../app.css';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/userStore';
  import Sidebar from './home/components/Sidebar.svelte';
  import TopBar from '$lib/components/TopBar.svelte';
  
  onMount(() => {
    const unsubscribe = user.subscribe((currentUser) => {
      const path = window.location.pathname;
      const protectedRoutes = ['/home', '/teams'];
      console.log("Current User: ", currentUser);
      console.log("Display Name: ", currentUser?.displayName);
      // if (!currentUser && protectedRoutes.some(route => path.startsWith(route))) {
      //   goto('/');
      // }
    });
    
    return () => {
      unsubscribe();
    };
  });

  $: showSidebar = $user && ['/home', '/teams'].some(route => window.location.pathname.startsWith(route));
</script>

<div class="min-h-screen bg-gray-100">
  {#if showSidebar}
    <TopBar />
    <div class="flex">
      <main class="flex-1">
        <div class="max-w-9x2 mx-auto py-6 sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
    </div>
  {:else}
    <slot />
  {/if}
</div>