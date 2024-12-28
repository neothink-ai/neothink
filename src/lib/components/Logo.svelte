<script>
  import { base } from '$app/paths';

  export let type = ''; // Default value

  let logoSrc;
  let logoAlt;

  console.log(type);

  $: {
    logoSrc = `assets/${type}.png`;
    logoAlt = `${type.charAt(0).toUpperCase() + type.slice(1)} Logo`;
  }
</script>

<a href="{base}/home" class="flex items-center space-x-2">
  <img
    src={logoSrc}
    alt={logoAlt}
    class="logo"
  />
  <!-- {type.charAt(0).toUpperCase() + type.slice(1)} -->
</a>

<style>
  .logo {
    width: 240px;
    height: 140px;
  }
</style>