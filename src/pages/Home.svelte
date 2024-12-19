<script>
  import { onMount } from "svelte";
  import lottie from "lottie-web";

  let animationContainer;

  // Load animation when the component mounts
  onMount(() => {
    lottie.loadAnimation({
      container: animationContainer,
      renderer: "svg",
      loop: true,
      autoplay: true,
      path: "/assets/ani1.json", // Replace with the correct path to your animation JSON file
    });
  });

  // Features Data
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

  <!-- Main Section -->
  <main class="main-container">
    <h1>Smarter Workflows, Smarter Teams</h1>
    <p>Plan. Optimize. Achieve. Powered by the brilliance of AI.</p>

    <div class="main-content">
      <div class="animation-container" bind:this={animationContainer}></div>
      <!-- Lottie animation container -->

      <!-- Buttons next to the animation -->
      <div class="buttons-container">
        <button class="button primary">Sign Up</button>
        <button class="button secondary">Learn More</button>
      </div>
    </div>
  </main>

  <!-- Features Section -->
  <section class="features">
    {#each features as feature}
      <div class="feature-card">
        <div class="icon-container">
          <img src={feature.icon} alt={feature.title} class="feature-icon" />
        </div>
        <strong>{feature.title}</strong>
        <p>{feature.description}</p>
      </div>
    {/each}
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-logo">
      <img src="/assets/neothink.png" alt="Footer Logo" />
    </div>
    <nav class="footer-nav">
      <a href="#">About us</a>
      <a href="#">Careers</a>
      <a href="#">Help</a>
      <a href="#">Privacy</a>
    </nav>
  </footer>
</div>

<style>
  /* General Styles */
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

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

  .button:hover {
    opacity: 0.9;
  }

  /* Features Section */
  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    width: 100%;
    margin: 40px auto;
    padding: 0 20px;
    text-align: center;
  }

  .feature-card {
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
    transition:
      transform 0.3s,
      box-shadow 0.3s;
  }

  .feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }

  .icon-container {
    background: #f8f9fa;
    border-radius: 50%;
    width: 150px; /* Increased size significantly */
    height: 150px; /* Increased size significantly */
    margin: 0 auto 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .feature-icon {
    width: 90%; /* The icon fills most of the container */
    height: 90%; /* Maintains 1:1 ratio */
    object-fit: contain;
  }

  .feature-card strong {
    display: block;
    font-size: 18px;
    margin-bottom: 10px;
    color: #333;
  }

  .feature-card p {
    font-size: 14px;
    color: #666;
  }

  .footer {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 40px;
    border-top: 1px solid #f0f0f0;
    padding-top: 20px;
    font-size: 14px;
  }

  .footer-logo img {
    width: 100px;
    height: auto;
  }

  .footer-nav a {
    text-decoration: none;
    color: gray;
    margin-left: 20px;
  }
</style>
