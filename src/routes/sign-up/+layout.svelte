<style>
    .background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('assets/feature1.png');
    background-size: cover;
    background-position: center;
    opacity: 0.5; /* Adjust the opacity as needed */
    z-index: -1; /* Ensure the background is behind the content */
  }
    .login-layout {
      justify-content: center;
    }

    /* Override padding for specific classes */
  </style>
  
  <div class="background"></div>
  <div class="login-layout">
    <slot />
  </div>