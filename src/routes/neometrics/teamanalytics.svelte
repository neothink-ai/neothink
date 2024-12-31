<script>
  import { onMount } from 'svelte';
  let teamData;

  onMount(async () => {
      const response = await fetch('/assets/team.json');
      teamData = await response.json();
  });
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Open+Sauce+Bold&display=swap');

  .members-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 20px;
  }

  .member {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
      background-color: white;
      border: 1px solid black;
      border-radius: 10px;
      padding: 10px;
      width: 300px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .member img {
      border-radius: 50%;
      border: 2px solid #00bf63;
      width: 50px;
      height: 50px;
      margin-right: 10px;
  }

  .member-name {
      color: black;
      font-weight: bold;
      font-family: 'Open Sauce Bold', sans-serif;
  }
</style>

{#if teamData}
  <div class="members-section">
      <h2>Members</h2>
      {#each teamData.members as member}
          <div class="member">
              <img src={`/assets/${member.name.toLowerCase()}.jpg`} alt={member.name} />
              <span class="member-name">{member.name}</span>
          </div>
      {/each}
  </div>
{/if}
