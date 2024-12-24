<script>
    import { authHandlers, error } from "$lib/firebase/authStore";
    import {signIn} from '$lib/firebase/auth'; 
    import { navigate } from "svelte-routing";
    import { Router, Route } from "svelte-routing"; // Add Route here
  
    let email = "";
    let password = "";
  
    // Handle Login
    async function handleLogin() {
      try {
        await signIn(email, password);
        // Redirect to home page or dashboard
        window.location.href = "/";
      } catch (err) {
        console.error("Login failed:", err);
        $error = "Invalid email or password.";
      }
    }
  
    // Handle Google Login
    async function handleGoogleAuth() {
      try {
        const user = await authHandlers.loginWithGoogle();
        console.log("User logged in with Google:", user);
        window.location.href = "/"; // Redirect on success
      } catch (err) {
        console.error("Google login failed:", err);
      }
    }
  </script>
  
  
  <!-- Loader Section -->
  <div id="loader" class="loader">
    <div class="spinner"></div>
  </div>
  
  <!-- Main Container (Login Form) -->
  <div class="container">
    <div class="header">
      <img src="assets/neothink.png" alt="Logo" class="logo" />
    </div>
    <h2>Log In</h2>
    <form on:submit|preventDefault={handleLogin}>
      <label for="email">Email</label>
      <input type="email" id="email" name="email" bind:value={email} required />
  
      <label for="password">Password</label>
      <input
        type="password"
        id="password"
        name="password"
        bind:value={password}
        required
      />
  
      <button type="submit" id="submit">Log In</button>
    </form>
  
    <!-- OAuth Buttons Section -->
    <div class="oauth-buttons">
      <button class="oauth google" on:click={handleGoogleAuth}>
        <img src="/assets/google.png" alt="Google Logo" class="oauth-logo" />
        Google
      </button>
      <button class="oauth microsoft" id="microsoftLogin">
        <img
          src="/assets/microsoft.png"
          alt="Microsoft Logo"
          class="oauth-logo"
        />
        Microsoft
      </button>
      <button class="oauth twitter" id="twitterLogin">
        <img src="/assets/twitter.jpg" alt="Twitter Logo" class="oauth-logo" />
        Twitter
      </button>
    </div>
  
    <p>
      Don't have an account? <a href='/sign-up'>Sign Up!</a>
  
      {#if $error}
        <p class="error">{$error}</p>
      {/if}
    </p>
  </div>
  
  <!-- Styles for Login.svelte -->
  <style>
    /* General Body Styles */
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 0;
    }
  
    /* Loader Styles */
    .loader {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background-color: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      visibility: hidden;
      opacity: 0;
      transition:
        opacity 0.3s ease,
        visibility 0.3s ease;
    }
  
    .spinner {
      border: 8px solid #f3f3f3;
      border-top: 8px solid #8b61c2;
      border-radius: 50%;
      width: 60px;
      height: 60px;
      animation: spin 2s linear infinite;
    }
  
    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  
    body.loading #loader {
      visibility: visible;
      opacity: 1;
    }
  
    /* Container Style */
    .container {
      max-width: 400px;
      margin: 50px auto;
      margin-top: 2%;
      background-color: #fff;
      padding: 20px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      border-radius: 12px;
    }
  
    /* Header Style */
    .header {
      text-align: center;
      margin-bottom: 20px;
    }
  
    .logo {
      width: 150px;
      height: auto;
    }
  
    /* Header Text Style */
    h2 {
      font-family: "Cormorant Garamond", serif;
      font-size: 24px;
      text-align: center;
      margin-bottom: 20px;
      color: #333;
    }
  
    /* Form Style */
    form {
      display: flex;
      flex-direction: column;
    }
  
    label {
      margin-bottom: 5px;
      color: #333;
    }
  
    input {
      margin-bottom: 15px;
      padding: 12px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      transition: border-color 0.3s ease;
    }
  
    input:focus {
      border-color: #8b61c2;
      outline: none;
    }
  
    /* Submit Button Style */
    button {
      padding: 12px;
      font-size: 16px;
      color: #fff;
      background-color: #8b61c2;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    button:hover {
      background-color: #7a4fa2;
    }
  
    /* OAuth Buttons Style */
    .oauth-buttons {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      margin-top: 20px;
    }
  
    .oauth {
      padding: 10px 12px;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      cursor: pointer;
      transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;
      width: 32%;
      color: #000;
    }
  
    .oauth:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
  
    .google:hover {
      border-color: #db4437;
      background-color: #f4b8b1;
    }
  
    .microsoft:hover {
      border-color: #00a4ef;
      background-color: #aad8f7;
    }
  
    .twitter:hover {
      border-color: #1da1f2;
      background-color: #a6d8f7;
    }
  
    .oauth-logo {
      width: 24px;
      margin-right: 10px;
    }
  
    /* Footer Link Style */
    p {
      text-align: center;
      margin-top: 20px;
    }
  
    a {
      color: #8b61c2;
      text-decoration: none;
    }
  
    a:hover {
      text-decoration: underline;
    }
  
    /* Error message style */
    .error {
      color: red;
      text-align: center;
      margin-top: 10px;
    }
  </style>
  