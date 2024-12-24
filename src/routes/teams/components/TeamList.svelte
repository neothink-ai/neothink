<script>
  import TeamCard from './TeamCard.svelte';
  
  export let teams = [];
  export let isAdmin = false;
  export let showControls = false;
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {#each teams as team (team.id)}
    <TeamCard {team} {isAdmin} {showControls} />
  {/each}
  
  {#if teams.length === 0}
    <p class="text-gray-500 col-span-full text-center py-8">
      No teams found
    </p>
  {/if}
</div>