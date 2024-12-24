<script>
  import { navigate } from "svelte-routing";
  let userType = "";
  let teamRole = "";
  let freelancerStatus = "";
  let focusArea = "";

  // Save user input and navigate based on the selection
  function handleSubmit() {
    const userAnswers = {
      userType,
      teamRole,
      freelancerStatus,
      focusArea,
    };

    // Here, we'll store data in Firebase
    saveUserData(userAnswers);

    // Redirect based on the type
    if (userType === "team") {
      if (teamRole === "admin") {
        navigate("/team-admin");
      } else {
        navigate("/team-member");
      }
    } else {
      navigate("/individual");
    }
  }
</script>

<div class="container mx-auto p-4">
  <h2 class="text-2xl mb-4">Tell us about yourself</h2>

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
      <label class="block text-lg"
        >Are you a Team or Individual Professional?</label
      >
      <select bind:value={userType} class="input">
        <option value="">Select...</option>
        <option value="team">Team</option>
        <option value="individual">Individual</option>
      </select>
    </div>

    {#if userType === "team"}
      <div>
        <label class="block text-lg">Are you a Team Admin or Team Member?</label
        >
        <select bind:value={teamRole} class="input">
          <option value="">Select...</option>
          <option value="admin">Admin</option>
          <option value="member">Member</option>
        </select>
      </div>
    {/if}

    {#if userType === "individual"}
      <div>
        <label class="block text-lg">Are you a Freelancer or Employee?</label>
        <select bind:value={freelancerStatus} class="input">
          <option value="">Select...</option>
          <option value="freelancer">Freelancer</option>
          <option value="employee">Employee</option>
        </select>
      </div>
    {/if}

    <div>
      <label class="block text-lg"
        >Are you focusing more on Developer or Manager tasks?</label
      >
      <select bind:value={focusArea} class="input">
        <option value="">Select...</option>
        <option value="developer">Developer</option>
        <option value="manager">Manager</option>
      </select>
    </div>

    <button type="submit" class="btn">Submit</button>
  </form>
</div>

<style>
  /* Tailwind CSS will style the form */
</style>
