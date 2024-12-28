<script>
	import { fade, fly } from 'svelte/transition';
	import { PRIORITY } from '$lib/models/task';
	import { auth } from '$lib/backend/firebase';
	
	export let tasks = [];
	export let onClose = () => {};
	export let selectedDate = null;
	
	let isAddingTask = false;
	let newTask = {
		task_name: '',
		description: '',
		timestamp: '',
		priority: PRIORITY.MEDIUM,
		hours: 1
	};
	
	function getPriorityColor(priority) {
		if (priority >= 4) return 'bg-green-100 border-green-200';
		if (priority >= 2) return 'bg-yellow-100 border-yellow-200';
		return 'bg-red-100 border-red-200';
	}
	
	async function handleAddTask() {
		try {
			if (!auth.currentUser) throw new Error('User not authenticated');
			
			// Set the date from selectedDate but keep the time from the time input
			const taskDate = new Date(selectedDate);
			const [hours, minutes] = newTask.timestamp.split(':').map(Number);
			taskDate.setHours(hours, minutes);
			
			
			const taskData = {
				...newTask,
				timestamp: taskDate.toISOString(),
				hours: parseFloat(newTask.hours)
			};
			console.log(taskData);
			
			await addTask(auth.currentUser.uid, taskData);
			isAddingTask = false;
			newTask = {
				task_name: '',
				description: '',
				timestamp: '',
				priority: PRIORITY.MEDIUM,
				hours: 1
			};
			
			// Refresh tasks list
			// You would typically implement a way to refresh the tasks list here
		} catch (error) {
			console.error('Error adding task:', error);
			alert('Failed to add task: ' + error.message);
		}
	}
</script>

<div
	class="fixed inset-0 bg-black/50 flex items-center justify-center"
	on:click={onClose}
	transition:fade={{ duration: 200 }}
>
	<div
		class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md"
		on:click|stopPropagation
		transition:fly={{ y: 20, duration: 300 }}
	>
		<div class="flex justify-between items-center mb-4">
			<h2 class="text-xl font-bold">Tasks</h2>
			<button
				class="text-gray-500 hover:text-gray-700"
				on:click={onClose}
			>
					✕
			</button>
		</div>
		
		{#if !isAddingTask}
			<div class="space-y-3">
				{#each tasks as task}
					<div class="p-4 rounded-lg border {getPriorityColor(task.priority)}">
						<div class="flex justify-between items-start">
							<span class="text-sm font-medium">{task.task_name}</span>
							<span class="text-sm text-gray-500">
								{new Date(task.timestamp).toLocaleTimeString()}
							</span>
						</div>
						<p class="mt-2 text-gray-700">{task.description}</p>
						<div class="mt-2 text-sm text-gray-600">
							Duration: {task.hours} hour{task.hours !== 1 ? 's' : ''}
						</div>
					</div>
				{/each}
				
				{#if tasks.length === 0}
					<p class="text-center text-gray-500">No tasks for this day</p>
				{/if}
				
				<button
					class="w-full mt-4 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
					on:click={() => isAddingTask = true}
				>
					Add Task
				</button>
			</div>
		{:else}
			<form
				class="space-y-4"
				on:submit|preventDefault={handleAddTask}
			>
				<div>
					<label for="task_name" class="block text-sm font-medium text-gray-700">
						Task Name
					</label>
					<input
						type="text"
						id="task_name"
						bind:value={newTask.task_name}
						class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
					/>
				</div>
				
				<div>
					<label for="description" class="block text-sm font-medium text-gray-700">
						Description
					</label>
					<textarea
						id="description"
						bind:value={newTask.description}
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
						rows="3"
						required
					></textarea>
				</div>
				
				<div>
					<label for="timestamp" class="block text-sm font-medium text-gray-700">
						Time
					</label>
					<input
						type="time"
						id="timestamp"
						bind:value={newTask.timestamp}
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
						required
					/>
				</div>
				
				<div>
					<label for="hours" class="block text-sm font-medium text-gray-700">
						Duration (hours)
					</label>
					<input
						type="number"
						id="hours"
						bind:value={newTask.hours}
						min="0.5"
						step="0.5"
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
						required
					/>
				</div>
				
				<div>
					<label for="priority" class="block text-sm font-medium text-gray-700">
						Priority
					</label>
					<select
						id="priority"
						bind:value={newTask.priority}
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
						required
					>
						<option value="1">1 (Low)</option>
						<option value="2">2</option>
						<option value="3">3 (Medium)</option>
						<option value="4">4</option>
						<option value="5">5 (High)</option>
					</select>
				</div>
				
				<div class="flex space-x-3">
					<button
						type="submit"
						class="flex-1 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
					>
						Save Task
					</button>
					<button
						type="button"
						class="flex-1 py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
						on:click={() => isAddingTask = false}
					>
						Cancel
					</button>
				</div>
			</form>
		{/if}
	</div>
</div>