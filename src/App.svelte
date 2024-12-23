<script>
  import { onMount } from 'svelte';
  import { navigate, Router, Route } from "svelte-routing";
  import SignUp from './routes/signup/SignUp.svelte';
  import Dashboard from '../src/components/Dashboard.svelte';
  import Home from '../src/pages/Home.svelte';
  import {user, loading} from '../src/lib/stores/authStore';

  onMount(() => {
        return user.subscribe(($user) => {
            if (!$loading && $user) {
                navigate('/dashboard');
            }
        });
    });
</script>

<!-- {#if $loading}
    <div class="loading">Loading...</div>
{:else}
    {#if $user}
        <Dashboard />
    {/if}
{/if} -->


<Router>
  <Route path = '/' component = {Home}/>
  <Route path = '/signup' component = {SignUp}/>
  <Route path = '/dashboard' component = {Dashboard} />
</Router>
<!-- <main>
  <Home />
</main> -->

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
  }

  main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
</style>
