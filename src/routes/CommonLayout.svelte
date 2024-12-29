<script>
  import Sidebar from '../lib/components/Sidebar.svelte';
  import TopBar from '$lib/components/TopBar.svelte';

  export let pageType = 'home';

  $: sidebarAppType = (() => {
    if (pageType === 'home') return 'neotaskmaster';
    if (pageType === 'about') return 'neothink';
    if (pageType.startsWith('neometrics')) return 'neometrics';
    if (pageType === 'kanban') return 'neoplan';
    return 'neoplan';
  })();
</script>

<div class="min-h-screen bg-gray-100">
  <TopBar logoType={sidebarAppType}/>
  <div class="flex h-[calc(100vh-64px)]">
    <Sidebar />
    <main class="flex-1 overflow-hidden pl-[80px]"> <!-- Changed ml-[80px] to pl-[80px] -->
      <div class="h-full w-full">
        <slot />
      </div>
    </main>
  </div>
</div>