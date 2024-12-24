<script>
	import { onMount } from 'svelte';
	import lottie from 'lottie-web';

	let animationContainer;

	onMount(async () => {
		const animationData = {
			// Simple animation data for demo
			v: "5.5.7",
			fr: 60,
			ip: 0,
			op: 180,
			w: 512,
			h: 512,
			nm: "Demo Animation",
			ddd: 0,
			assets: [],
			layers: [{
				ty: 4,
				nm: "Shape Layer",
				sr: 1,
				ks: {
					o: { a: 0, k: 100 },
					r: { a: 1, k: [{ t: 0, s: [0], h: 0 }, { t: 180, s: [360] }] },
					p: { a: 0, k: [256, 256, 0] },
					a: { a: 0, k: [0, 0, 0] },
					s: { a: 0, k: [100, 100, 100] }
				},
				ao: 0,
				shapes: [{
					ty: "rc",
					d: 1,
					s: { a: 0, k: [100, 100] },
					p: { a: 0, k: [0, 0] },
					r: { a: 0, k: 0 },
					nm: "Rectangle",
					mn: "ADBE Vector Shape - Rect",
					hd: false
				}],
				ip: 0,
				op: 180,
				st: 0,
				bm: 0
			}]
		};

		lottie.loadAnimation({
			container: animationContainer,
			renderer: 'svg',
			loop: true,
			autoplay: true,
			animationData
		});
	});
</script>

<div class="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600 p-4">
	<div class="mb-8 w-64 h-64" bind:this={animationContainer}></div>
	
	<div class="text-center">
		<h1 class="mb-6 text-5xl font-bold text-white">Welcome to Our App</h1>
		<p class="mb-8 text-xl text-white/90">Experience the future of web applications</p>
		
		<div class="space-x-4">
			<a
				href="/sign-up"
				class="rounded-lg bg-white px-6 py-3 font-semibold text-blue-600 shadow-lg hover:bg-blue-50 transition-colors"
			>
				Get Started
			</a>
			<a
				href="/home"
				class="rounded-lg border-2 border-white px-6 py-3 font-semibold text-white hover:bg-white/10 transition-colors"
			>
				Learn More
			</a>
		</div>
	</div>
</div>