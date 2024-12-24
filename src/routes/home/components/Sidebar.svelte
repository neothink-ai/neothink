<script>
  const menuItems = [
    { label: 'Dashboard', icon: '📊', href: '/home' },
    { label: 'Teams', icon: '👥', href: '/teams' },
    { label: 'Projects', icon: '📁', href: '/projects' },
    { label: 'Messages', icon: '✉️', href: '/messages' }
  ];
</script>

<aside class="h-screen w-64 bg-gray-800 p-4 flex flex-col">
  <div class="mb-8">
    <h2 class="text-xl font-bold text-white">App Name</h2>
  </div>
  
  <nav class="flex-1">
    {#each menuItems as item}
      <a
        href={item.href}
        class="w-full mb-2 flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 rounded-lg transition-colors"
      >
        <span class="mr-3">{item.icon}</span>
        {item.label}
      </a>
    {/each}
  </nav>
</aside>