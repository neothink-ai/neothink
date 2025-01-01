<script>
  import { onMount } from 'svelte';
  import { user } from '../../lib/stores/userStore';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  let teams = writable([]);
  let tasks = writable([]);
  let prompt = '';
  let isLoading = writable(false);
  let selectedAssignees = writable({});

  onMount(async () => {
    const userId = $user?.uid;
    if (userId) {
      try {
        // Change the fetching teams route to return back the users in the payload itself
        const response = await axios.get(`/teams/user/${userId}`); 
        teams.set(response.data);
      } catch (error) {
        console.error('Error fetching teams:', error);
      }
    }
  });

  async function handlePromptSubmit() {
    isLoading.set(true);
    try {
      const response = await axios.post('/process-json', { key: 'prompt', value: prompt });
      let json_response = JSON.parse(response.data);
      tasks.set(json_response.tasks);
    } catch (error) {
      console.error('Error processing prompt:', error);
    } finally {
      isLoading.set(false);
    }
  }

  async function addProject() {
    const tasksData = $tasks.map(task => ({
      ...task,
      assignee: selectedAssignees[task._id] || null
    }));
    try {
      await axios.post('/tasks', tasksData);
      alert('Project added successfully');
    } catch (error) {
      console.error('Error adding project:', error);
    }
  }
</script>

<div class="container">
    <div class="team-members">
        <h2>Team Members</h2>
        {#each $teams as team}
            <div class="team">
                <h3>{team.name}</h3>
                <ul>
                    {#each team.users as user}
                        <li>{user}</li>
                    {/each}
                </ul>
            </div>
        {/each}
    </div>
  <div class="tasks">
    {#each $tasks as task}
      <div class="task-card">
        <h3>{task.title}</h3>
        <p>{task.description}</p>
        <p>Deadline: {task.deadline}</p>
        <div class="dropdown">
          <label for="assignee">Assign to:</label>
          <select id="assignee" bind:value={$selectedAssignees[task._id]}>
            {#each $teams as team}
              {#each team.users as user}
                <option value={user}>{user}</option>
              {/each}
            {/each}
          </select>
        </div>
      </div>
    {/each}
  </div>

  {#if $isLoading}
    <p>Getting you the best roadmap...</p>
  {/if}

  <button on:click={addProject}>Add Project</button>
</div>

<footer class="footer">
  <textarea
    class="textbox"
    bind:value={prompt}
    placeholder="Plan your project with neoplan"
    rows="3"
    on:keydown={(e) => e.key === 'Enter' && handlePromptSubmit()}
  ></textarea>
</footer>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin-bottom: 100px; /* Ensure there's space for the footer */
    width: 100%;
    box-sizing: border-box;
  }
  .tasks {
    width: 100%;
    max-width: 800px; /* Adjust as needed */
  }
  .footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: white;
    padding: 10px;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  }
  .textbox {
    width: 100%;
    max-width: 90%; /* Adjust as needed */
    margin: 0 3%;
    padding: 10px;
    border: 1px solid gray;
    border-radius: 5px;
    box-sizing: border-box;
  }
  .tasks {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }
  .task-card {
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 8px;
    width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .dropdown {
    margin-top: 10px;
  }
</style>