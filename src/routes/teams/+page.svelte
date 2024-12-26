<script>
  //teams page
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/userStore';
  import { getUserTeamsDetails } from '$lib/firebase/users';
  import { getAllTeams } from '$lib/firebase/teams';

  let userTeams = [];
  let allTeams = [];
  let loading = true;

  onMount(async () => {
    if ($user) {
      try {
        const userTeamsData = await getUserTeamsDetails($user.uid);
        userTeams = userTeamsData;
        if ($user.isAdmin) {
          allTeams = await getAllTeams();
        }
      } catch (error) {
        console.error('Error loading teams:', error);
      } finally {
        loading = false;
      }
    }
  });
</script>

<style>
  .team-block {
    transition: transform 0.3s ease;
  }
  .team-block:hover {
    transform: scale(1.1);
  }
</style>

<div class="flex min-h-screen bg-gray-100">
  <main class="flex-1 p-8">
    {#if loading}
      <div class="flex justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    {:else}
      <section class="mb-12">
        <h2 class="text-2xl font-bold mb-6">Your Teams</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each userTeams as team}
            <div class="team-block p-4 bg-white shadow rounded-lg">
              <h3 class="text-xl font-semibold">{team.name}</h3>
              <p>{team.description}</p>
            </div>
          {/each}
        </div>
      </section>

      {#if $user?.isAdmin}
        <section>
          <h2 class="text-2xl font-bold mb-6">All Teams</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each allTeams as team}
              <div class="team-block p-4 bg-white shadow rounded-lg">
                <h3 class="text-xl font-semibold">{team.name}</h3>
                <p>{team.description}</p>
              </div>
            {/each}
          </div>
        </section>
      {/if}
    {/if}
  </main>
</div>