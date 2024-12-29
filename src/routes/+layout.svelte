<script>
  import '../app.css';
  import CommonLayout from './CommonLayout.svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { auth } from '$lib/firebase/firebase';
  import { authStore } from '$lib/stores/authStore';

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

  // Define routes that should use CommonLayout
  $: showCommonLayout = ['/home', '/teams', '/about', '/neotaskmaster', '/kanban', '/neometrics']
    .some(route => $page.url.pathname.startsWith(route));

  // Extract the page type from the URL
  $: pageType = $page.url.pathname.slice(1);
</script>

{#if showCommonLayout}
  <CommonLayout {pageType}>
    <slot />
  </CommonLayout>
{:else}
  <slot />
{/if}