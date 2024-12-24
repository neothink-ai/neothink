<script>
	import Sidebar from './components/Sidebar.svelte';
	import ProfileMenu from './components/ProfileMenu.svelte';
	import Calendar from './components/Calendar.svelte';
</script>

<div class="flex min-h-screen bg-gray-100">
	<Sidebar />
	
	<main class="flex-1 p-8">
		<div class="flex justify-end mb-8">
			<ProfileMenu />
		</div>
		
		<div class="max-w-3xl mx-auto">
			<Calendar />
		</div>
	</main>
</div>