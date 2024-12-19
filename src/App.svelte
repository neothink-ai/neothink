<script>
  import Home from "./pages/Home.svelte";
</script>

<main>
  <Home />
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
  }

  main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
</style>
