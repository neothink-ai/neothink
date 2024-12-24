<script>
	import { onMount } from 'svelte';
	import { getDaysInMonth, formatDate } from '$lib/utils/date';
	import TaskModal from './TaskModal.svelte';
	import { auth } from '$lib/firebase/firebase';
	import { getTasksForDate } from '$lib/firebase/tasks';
	
	let currentDate = new Date();
	let daysInMonth = [];
	let selectedDate = null;
	let tasks = [];
	
	async function loadTasks(date) {
		if (!auth.currentUser) return;
		try {
			tasks = await getTasksForDate(auth.currentUser.uid, date);
		} catch (error) {
			console.error('Error loading tasks:', error);
			tasks = [];
		}
	}
	
	function updateMonth(increment) {
		currentDate = new Date(
			currentDate.getFullYear(),
			currentDate.getMonth() + increment,
			1
		);
		daysInMonth = getDaysInMonth(currentDate);
	}
	
	async function selectDay(day) {
		if (!day) return;
		
		selectedDate = new Date(
			currentDate.getFullYear(),
			currentDate.getMonth(),
			day
		);
		
		await loadTasks(selectedDate);
	}
	
	onMount(() => {
		daysInMonth = getDaysInMonth(currentDate);
	});
	
	const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
	const months = [
		'January', 'February', 'March', 'April', 'May', 'June',
		'July', 'August', 'September', 'October', 'November', 'December'
	];
</script>

<div class="bg-white rounded-lg shadow p-6">
	<div class="flex justify-between items-center mb-4">
		<h2 class="text-xl font-bold">
			{months[currentDate.getMonth()]} {currentDate.getFullYear()}
		</h2>
		<div class="space-x-2">
			<button
				class="p-2 hover:bg-gray-100 rounded-lg"
				on:click={() => updateMonth(-1)}
			>
				←
			</button>
			<button
				class="p-2 hover:bg-gray-100 rounded-lg"
				on:click={() => updateMonth(1)}
			>
				→
			</button>
		</div>
	</div>
	
	<div class="grid grid-cols-7 gap-2">
		{#each weekDays as day}
			<div class="text-center text-sm font-medium text-gray-500 py-2">
				{day}
			</div>
		{/each}
		
		{#each daysInMonth as day}
			{#if day !== null}
				<button
					class="aspect-square flex flex-col items-center justify-center border rounded-lg
						hover:bg-gray-50 relative"
					on:click={() => selectDay(day)}
				>
					<span>{day}</span>
				</button>
			{:else}
				<div class="aspect-square"></div>
			{/if}
		{/each}
	</div>
</div>

{#if selectedDate}
	<TaskModal
		{tasks}
		{selectedDate}
		onClose={() => {
			selectedDate = null;
			tasks = [];
		}}
	/>
{/if}