<script>
  import { onMount } from "svelte";
  import lottie from "lottie-web";

  let animationContainer;

  // Load the Lottie animation on mount
  onMount(() => {
    lottie.loadAnimation({
      container: animationContainer,
      renderer: "svg",
      loop: true,
      autoplay: true,
      path: "/assets/ani1.json", // Update the path to the animation JSON
    });
  });

  // Features data
  const features = [
    {
      icon: "/assets/1.png",
      title: "Workflows",
      description: "Design workflows, share ideas.",
    },
    {
      icon: "/assets/2.png",
      title: "Communication",
      description: "Create smarter processes and communicate seamlessly.",
    },
    {
      icon: "/assets/3.png",
      title: "Knowledge",
      description: "One hub for your team's intelligence.",
    },
    {
      icon: "/assets/4.png",
      title: "Precision",
      description: "Centralize knowledge, streamline collaboration.",
    },
    {
      icon: "/assets/5.png",
      title: "Success",
      description: "Deliver every project with precision.",
    },
    {
      icon: "/assets/6.png",
      title: "Goals",
      description: "Plan, execute, and track progress from start to finish.",
    },
    {
      icon: "/assets/7.png",
      title: "Neothink AI",
      description: "Answers at your fingertips.",
    },
    {
      icon: "/assets/8.png",
      title: "Schedule",
      description: "Your schedule, all in one view.",
    },
  ];
</script>

<div class="container">
  <!-- Header -->
  <header class="header">
    <div class="header-logo">
      <img src="/assets/neothink.png" alt="Logo" />
    </div>
    <nav class="header-nav">
      <a href="#">Product</a>
      <a href="#">Teams</a>
      <a href="#">Individuals</a>
      <a href="#">Pricing</a>
    </nav>
  </header>

  <!-- Hero Section -->
  <main class="main-container">
    <h1>Smarter Workflows, Smarter Teams</h1>
    <p>Plan. Optimize. Achieve. Powered by the brilliance of AI.</p>

    <div class="main-content">
      <div class="animation-container" bind:this={animationContainer}></div>
      <div class="buttons-container">
        <button class="button primary">Sign Up</button>
        <button class="button secondary">Learn More</button>
      </div>
    </div>
  </main>

  <!-- Key Features Section -->
  <section class="key-features">
    <h2>Explore Neothink's Core Features</h2>
    <div class="feature-cards">
      <div class="key-feature-card">
        <div class="card-header">
          <img src="/assets/neotaskmaster.png" alt="Neotaskmaster" />
        </div>
        <div class="card-body">
          <h3>Neotaskmaster</h3>
          <p>
            Smart AI Task Management with assignment and scheduling
            capabilities.
          </p>
        </div>
      </div>
      <div class="key-feature-card">
        <div class="card-header">
          <img src="/assets/neometrics.png" alt="Neometrics" />
        </div>
        <div class="card-body">
          <h3>Neometrics</h3>
          <p>
            Advanced AI Data Analytics for tracking productivity and
            performance.
          </p>
        </div>
      </div>
      <div class="key-feature-card">
        <div class="card-header">
          <img src="/assets/neoplan.png" alt="Neoplan" />
        </div>
        <div class="card-body">
          <h3>Neoplan</h3>
          <p>
            Intelligent Project Management System for roadmap and task handling.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <h2>Core Features</h2>
    <div class="feature-cards">
      {#each features as feature}
        <div class="feature-card">
          <img src={feature.icon} alt={feature.title} class="feature-icon" />
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-logo">
      <img src="/assets/neothink.png" alt="Footer Logo" />
    </div>
    <nav class="footer-nav">
      <a href="#">About Us</a>
      <a href="#">Careers</a>
      <a href="#">Help</a>
      <a href="#">Privacy</a>
    </nav>
  </footer>
</div>

<style>
  /* General Styling */
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Header Styling */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
  }

  .header-logo img {
    width: 200px;
    height: auto;
  }

  .header-nav a {
    margin-left: 20px;
    text-decoration: none;
    color: black;
    font-weight: 600;
  }

  /* Hero Section */
  .main-container {
    text-align: center;
    margin-bottom: 40px;
  }

  .main-container h1 {
    font-size: 48px;
    margin-bottom: 10px;
  }

  .main-container p {
    font-size: 18px;
    margin-bottom: 30px;
    color: gray;
  }

  .main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
  }

  .animation-container {
    width: 300px;
    height: 300px;
  }

  .buttons-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .button {
    padding: 12px 25px;
    font-size: 16px;
    border: none;
    cursor: pointer;
    border-radius: 8px;
  }

  .button.primary {
    background-color: #0052cc;
    color: white;
    box-shadow: 0 4px 8px rgba(0, 82, 204, 0.4);
  }

  .button.secondary {
    background-color: #f0f0f0;
    color: black;
    border: 2px solid #0052cc;
    box-shadow: 0 4px 8px rgba(0, 82, 204, 0.1);
  }

  /* Key Features Section */
  .key-features {
    margin-top: 60px;
    width: 100%;
    text-align: center;
  }

  .key-features h2 {
    font-size: 36px;
    margin-bottom: 40px;
    font-family: "Georgia", serif;
  }

  .feature-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }

  .key-feature-card {
    background: #f9f9f9;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition:
      transform 0.3s,
      box-shadow 0.3s;
  }

  .key-feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }

  .card-header img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .card-body {
    padding: 20px;
  }

  .card-body h3 {
    font-size: 24px;
    margin-bottom: 10px;
    color: #333;
  }

  .card-body p {
    font-size: 16px;
    color: #555;
  }

  /* Features Section */
  .features {
    width: 100%;
    text-align: center;
    margin: 40px 0;
  }

  .features h2 {
    font-size: 36px;
    margin-bottom: 30px;
  }

  .feature-cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }

  .feature-card {
    background: #f8f8f8;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    width: 200px;
    text-align: center;
    padding: 20px;
    transition:
      transform 0.3s,
      box-shadow 0.3s;
  }

  .feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }

  .feature-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 15px;
    object-fit: contain;
  }

  .feature-card h3 {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .feature-card p {
    font-size: 14px;
    color: #555;
  }

  /* Footer */
  .footer {
    margin-top: 40px;
    text-align: center;
  }

  .footer-logo img {
    width: 200px;
  }

  .footer-nav a {
    margin: 0 15px;
    text-decoration: none;
    color: gray;
  }

  .footer-nav a:hover {
    color: black;
  }
</style>
