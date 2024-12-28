<script>
  import '../app.css';
  import Sidebar from '../lib/components/Sidebar.svelte';
  import TopBar from '$lib/components/TopBar.svelte';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/userStore';

  
  onMount(() => {
    console.log($user)
    // if (!$user) {
    //   goto('/login');
    // }
  });
</script>

<div class="min-h-screen bg-gray-100">
  <TopBar />
  <div class="flex">
    <Sidebar />
    <main class="flex-1">
      <div class="w-full max-w-9x2 mx-auto py-6 sm:px-6 lg:px-8">
        <slot />
      </div>
    </main>
  </div>
</div>