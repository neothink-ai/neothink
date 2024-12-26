<script>
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/userStore';
  import { getUserProfile, updateUserProfile, getUserTeamsDetails } from '$lib/firebase/users';

  let profile = null;
  let teams = [];
  let loading = true;
  let editing = false;
  let formData = {};
  let error = '';

  onMount(async () => {
    if ($user) {
      try {
        const userData = await getUserProfile($user.uid);
        profile = userData;
        formData = {
          firstName: userData.firstName,
          lastName: userData.lastName,
          department: userData.department,
          skills: [...userData.skills]
        };
        
        if (userData.teams?.length) {
          teams = await Promise.all(userData.teams.map(teamId => getUserTeamsDetails(teamId)));
        }
      } catch (err) {
        error = err.message;
      } finally {
        loading = false;
      }
    }
  });

  async function handleSubmit() {
    try {
      await updateUserProfile($user.uid, formData);
      profile = { ...profile, ...formData };
      editing = false;
      error = '';
    } catch (err) {
      error = err.message;
    }
  }

  function addSkill() {
    formData.skills = [...formData.skills, ''];
  }

  function removeSkill(index) {
    formData.skills = formData.skills.filter((_, i) => i !== index);
  }
</script>

<div class="flex min-h-screen bg-gray-100">
  <main class="flex-1 p-8"></main>
    {#if loading}
      <div class="flex justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    {:else if error}
      <div class="bg-red-50 text-red-600 p-4 rounded-lg mb-4">
        {error}
      </div>
    {:else}
      <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold">Profile Information</h1>
          <button
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            on:click={() => editing = !editing}
          >
            {editing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {#if editing}
          <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Department</label>
              <input
                type="text"
                bind:value={formData.department}
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Skills</label>
              {#each formData.skills as skill, i}
                <div class="flex space-x-2 mt-2">
                  <input
                    type="text"
                    bind:value={formData.skills[i]}
                    class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <button
                    type="button"
                    on:click={() => removeSkill(i)}
                    class="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </div>
              {/each}
              <button
                type="button"
                on:click={addSkill}
                class="mt-2 text-blue-600 hover:text-blue-800"
              >
                Add Skill
              </button>
            </div>

            <button
              type="submit"
              class="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Save Changes
            </button>
          </form>
        {:else}
          <div class="space-y-4">
            <div>
              <h2 class="text-sm font-medium text-gray-500">First Name</h2>
              <p class="mt-1">{profile.firstName}</p>
            </div>

            <div>
              <h2 class="text-sm font-medium text-gray-500">Last Name</h2>
              <p class="mt-1">{profile.lastName}</p>
            </div>

            <div>
              <h2 class="text-sm font-medium text-gray-500">Department</h2>
              <p class="mt-1">{profile.department}</p>
            </div>

            <div>
              <h2 class="text-sm font-medium text-gray-500">Skills</h2>
              <div class="mt-1 flex flex-wrap gap-2">
                {#each profile.skills as skill}
                  <span class="px-2 py-1 bg-gray-100 rounded-full text-sm">
                    {skill}
                  </span>
                {/each}
              </div>
            </div>

            <div>
              <h2 class="text-sm font-medium text-gray-500">Teams</h2>
              <div class="mt-2 space-y-2">
                {#each teams as team}
                  <div class="p-3 bg-gray-50 rounded-lg"></div>
                    <h3 class="font-medium">{team.name}</h3>
                    <p class="text-sm text-gray-600">Created: {new Date(team.createdAt).toLocaleDateString()}</p>
                  </div>
                {/each}
              </div>
            </div>
          </div>
        {/if}
      </div>
    {/if}
  </main>
</div>
