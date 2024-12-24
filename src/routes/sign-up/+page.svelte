<script>
	import { signUp } from '$lib/firebase/auth';
	
	let email = '';
	let password = '';
	let error = '';
	
	async function handleSubmit() {
		try {
			error = '';
			await signUp(email, password);
		} catch (e) {
			error = e.message;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-100">
	<div class="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
		<h1 class="mb-6 text-2xl font-bold text-gray-900">Sign Up</h1>
		
		{#if error}
			<div class="mb-4 rounded-md bg-red-50 p-4 text-red-700">
				{error}
			</div>
		{/if}
		
		<form class="space-y-4" on:submit|preventDefault={handleSubmit}>
			<div>
				<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
				<input
					type="email"
					id="email"
					bind:value={email}
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
					placeholder="Enter your email"
					required
				/>
			</div>
			<div>
				<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
				<input
					type="password"
					id="password"
					bind:value={password}
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
					placeholder="Create a password"
					required
				/>
			</div>
			<button
				type="submit"
				class="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
			>
				Sign Up
			</button>
		</form>
	</div>
</div>