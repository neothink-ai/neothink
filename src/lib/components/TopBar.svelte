<script>
  import Logo from './Logo.svelte';
  import ProfileMenu from '../../routes/home/components/ProfileMenu.svelte';
</script>

<header class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <Logo />
      <ProfileMenu />
    </div>
  </div>
</header>