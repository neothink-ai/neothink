<script>
	import { onMount } from 'svelte';
	import { getDaysInMonth, formatDate } from '$lib/utils/date';
	import TaskModal from './TaskModal.svelte';
	import { auth } from '$lib/backend/firebase';
	import {getUserTasksForDate} from '$lib/backend/users';
	import {user} from '$lib/stores/userStore';
	
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

<div class="calendar-container">
	<div class="calendar-header">
		<h2 class="calendar-title">
			{months[currentDate.getMonth()]} {currentDate.getFullYear()}
		</h2>
		<div class="calendar-controls">
			<button class="calendar-button" on:click={() => updateMonth(-1)}>←</button>
			<button class="calendar-button" on:click={() => updateMonth(1)}>→</button>
		</div>
	</div>
	
	<div class="calendar-grid">
		{#each weekDays as day}
			<div class="calendar-weekday">{day}</div>
		{/each}
		
		{#each daysInMonth as day}
			{#if day !== null}
				<button class="calendar-day" on:click={() => selectDay(day)}>
					<span>{day}</span>
				</button>
			{:else}
				<div class="calendar-empty-day"></div>
			{/if}
		{/each}
	</div>
</div>

{#if selectedDate}
	tasks = getUserTasksForDate($user.uid, selectedDate.toISOString());
	<TaskModal
		{tasks}
		{selectedDate}
		onClose={() => {
			selectedDate = null;
			tasks = [];
		}}
	/>
	/>
{/if}

<style>
	.calendar-container {
		background-color: #ffffff;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(9, 30, 66, 0.1);
		padding: 24px;
	}

	.calendar-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16px;
	}

	.calendar-title {
		font-size: 18px;
		font-weight: 600;
		color: #172b4d;
	}

	.calendar-controls {
		display: flex;
		gap: 8px;
	}

	.calendar-button {
		padding: 8px;
		border-radius: 4px;
		background-color: #ebecf0;
		border: none;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.calendar-button:hover {
		background-color: #d0d7de;
	}

	.calendar-grid {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 8px;
	}

	.calendar-weekday {
		text-align: center;
		font-size: 14px;
		font-weight: 500;
		color: #5e6c84;
		padding: 8px 0;
	}

	.calendar-day {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 16px;
		border-radius: 4px;
		background-color: #f4f5f7;
		border: none;
		cursor: pointer;
		transition: background-color 0.2s ease, transform 0.2s ease;
	}

	.calendar-day:hover {
		background-color: #ebecf0;
		transform: translateY(-2px);
		box-shadow: 0 4px 6px rgba(9, 30, 66, 0.15);
	}

	.calendar-empty-day {
		padding: 16px;
	}

	.calendar-day span {
		font-size: 14px;
		color: #172b4d;
	}
</style>