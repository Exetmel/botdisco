/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

addEventListener('fetch', (event) => {
	event.respondWith(handleRequest(event.request));
});

async function handleRequest() {
	// Load Pyodide
	const pyodide = await loadPyodide();

	// Fetch the Python file content
	const pythonFileUrl = './channelBot.py'; // Replace with your file URL
	const response = await fetch(pythonFileUrl);
	const pythonCode = await response.text();

	// Run the Python code
	pyodide.runPython(pythonCode);

	return new Response('Python code executed successfully!', {
		headers: { 'content-type': 'text/plain' },
	});
}

async function loadPyodide() {
	const pyodideUrl = 'https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js';
	await importScripts(pyodideUrl);
	return await pyodide.loadPyodide();
}
