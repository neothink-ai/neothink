<script>
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/userStore';
  import TeamList from './components/TeamList.svelte';
  import Sidebar from '../home/components/Sidebar.svelte';
  import ProfileMenu from '../home/components/ProfileMenu.svelte';
  import { getUserTeams, getAllTeams } from '$lib/firebase/teams';

  let userTeams = [];
  let allTeams = [];
  let loading = true;

  onMount(async () => {
    if ($user) {
      try {
        const [userTeamsData, allTeamsData] = await Promise.all([
          getUserTeams($user.uid),
          $user.isAdmin ? getAllTeams() : []
        ]);
        userTeams = userTeamsData;
        allTeams = allTeamsData;
      } catch (error) {
        console.error('Error loading teams:', error);
      } finally {
        loading = false;
      }
    }
  });
</script>

<div class="flex min-h-screen bg-gray-100">
  <Sidebar />
  
  <main class="flex-1 p-8">
    <div class="flex justify-end mb-8">
      <ProfileMenu />
    </div>

    {#if loading}
      <div class="flex justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    {:else}
      <section class="mb-12">
        <h2 class="text-2xl font-bold mb-6">Your Teams</h2>
        <TeamList teams={userTeams} isAdmin={$user?.isAdmin} />
      </section>

      {#if $user?.isAdmin}
        <section>
          <h2 class="text-2xl font-bold mb-6">All Teams</h2>
          <TeamList teams={allTeams} isAdmin={true} showControls={true} />
        </section>
      {/if}
    {/if}
  </main>
</div>