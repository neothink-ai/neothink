<script>
  import '../app.css';
  import CommonLayout from './CommonLayout.svelte';
  import { page } from '$app/stores';

  // Determine if the CommonLayout should be shown based on the route
  $: showCommonLayout = ['/home', '/teams', '/about', '/neotaskmaster'].some(route => $page.url.pathname.startsWith(route));
</script>

<div class="min-h-screen bg-gray-100">
  {#if showCommonLayout}
    <CommonLayout>
      <slot />
    </CommonLayout>
  {:else}
    <main class="flex-1">
      <div class="w-full py-6 sm:px-6 lg:px-8">
        <slot />
      </div>
    </main>
  {/if}
</div>