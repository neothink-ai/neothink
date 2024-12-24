<script>
  import { addMemberToTeam, removeMemberFromTeam } from '$lib/firebase/teams';
  
  export let team;
  export let isAdmin = false;
  export let showControls = false;
  
  let showMembers = false;
  let addingMember = false;
  let newMemberEmail = '';
  
  async function handleAddMember() {
    try {
      // In a real app, you'd first query the users collection to get the userId from email
      const userId = 'user-id-from-email';
      await addMemberToTeam(team.id, userId);
      newMemberEmail = '';
      addingMember = false;
    } catch (error) {
      console.error('Error adding member:', error);
    }
  }
  
  async function handleRemoveMember(userId) {
    try {
      await removeMemberFromTeam(team.id, userId);
    } catch (error) {
      console.error('Error removing member:', error);
    }
  }
</script>

<div class="bg-white rounded-lg shadow-md p-6">
  <div class="flex justify-between items-start mb-4">
    <div>
      <h3 class="text-xl font-semibold">{team.name}</h3>
      <p class="text-gray-600">{team.description}</p>
    </div>
    {#if showControls}
      <button
        class="text-blue-600 hover:text-blue-800"
        on:click={() => showMembers = !showMembers}
      >
        {showMembers ? 'Hide Members' : 'Show Members'}
      </button>
    {/if}
  </div>
  
  {#if showMembers}
    <div class="mt-4 space-y-2">
      <h4 class="font-medium">Team Members</h4>
      <ul class="space-y-2">
        {#each team.members as member}
          <li class="flex justify-between items-center">
            <span>{member.email}</span>
            {#if isAdmin}
              <button
                class="text-red-600 hover:text-red-800"
                on:click={() => handleRemoveMember(member.id)}
              >
                Remove
              </button>
            {/if}
          </li>
        {/each}
      </ul>
      
      {#if isAdmin}
        {#if addingMember}
          <form on:submit|preventDefault={handleAddMember} class="mt-4">
            <input
              type="email"
              bind:value={newMemberEmail}
              placeholder="Enter member email"
              class="w-full px-3 py-2 border rounded-lg"
            />
            <div class="mt-2 flex space-x-2">
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Add
              </button>
              <button
                type="button"
                class="px-4 py-2 border rounded-lg hover:bg-gray-50"
                on:click={() => addingMember = false}
              >
                Cancel
              </button>
            </div>
          </form>
        {:else}
          <button
            class="mt-4 text-blue-600 hover:text-blue-800"
            on:click={() => addingMember = true}
          >
            Add Member
          </button>
        {/if}
      {/if}
    </div>
  {/if}
</div>