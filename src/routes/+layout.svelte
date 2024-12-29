<script>
  import '../app.css';
  import CommonLayout from './CommonLayout.svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { auth } from '$lib/firebase/firebase';
  import { authStore } from '$lib/stores/authStore';

  // Initialize auth listener only once
  onMount(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      authStore.update(state => ({
        ...state,
        user,
        loading: false
      }));
    });

    return () => unsubscribe();
  });

  $: showCommonLayout = ['/home', '/teams', '/about', '/neotaskmaster', '/kanban', '/neometrics']
    .some(route => $page.url.pathname.startsWith(route));
</script>

<div class="min-h-screen">
  {#if showCommonLayout}
    <CommonLayout pageType={$page.url.pathname.slice(1)}>
      <slot />
    </CommonLayout>
  {:else}
    <main class="flex-1">
      <div class="w-full">
        <slot />
      </div>
    </main>
  {/if}
</div>