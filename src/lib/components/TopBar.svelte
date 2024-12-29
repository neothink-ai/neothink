<script>
  import Logo from './Logo.svelte';
  import ProfileMenu from './ProfileMenu.svelte';

  export let logoType = ''; // Default value
  console.log("Received logo type"); 
  console.log(logoType);
</script>

<header class="bg-white shadow-sm">
  <div class="max-w-8xl mx-auto">
    <div class="flex justify-between items-center h-16">
      <Logo type={logoType} />
      <ProfileMenu />
    </div>
  </div>
</header>