<script>
  import '../app.css';
  import Sidebar from '../lib/components/Sidebar.svelte';
  import TopBar from '$lib/components/TopBar.svelte';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, isLoading } from '$lib/stores/userStore';

  export let pageType = 'home'; // Default value
  console.log("Printing page type");
  console.log(pageType);
  let sidebarAppType;

  $: {
    if (pageType === 'home') {
      sidebarAppType = 'neotaskmaster';
    } else if (pageType === 'about') {
      sidebarAppType = 'neothink';
    } else if (pageType === 'neometrics' || pageType === 'neometrics/personal' || pageType === 'neometrics/team') {
      console.log("Setting it to neometrics");
      sidebarAppType = 'neometrics';
    } else if (pageType === 'kanban') {
      sidebarAppType = 'neoplan';
    } else {
      sidebarAppType = 'neoplan'; // Default value
    }
  }

  onMount(() => {
    console.log($user);
    console.log($isLoading);
    // if (!$user && !$isLoading) {
    //   goto('/login');``
    // }
  });
</script>

<div class="min-h-screen bg-gray-100">
  <TopBar logoType={sidebarAppType}/>
  <div class="flex">
    <Sidebar  />
    <main class="flex-1">
      <div class="w-full max-w-9x2 mx-auto py-6 sm:px-6 lg:px-8">
        <slot />
      </div>
    </main>
  </div>
</div>