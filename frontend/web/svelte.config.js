// frontend/web/svelte.config.js
// Configuration for SvelteKit to build the Vacation Planner web app.

import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    // We're not using an adapter for now to simplify development
    // This will use the default in-memory adapter
    paths: {
      base: '' // Set to '/your-base-path' if deploying to a subdirectory
    }
  }
};

export default config;

// Notes:
// - Using the default in-memory adapter for development.
// - For production, you would add an adapter like '@sveltejs/adapter-auto' or '@sveltejs/adapter-static'.
// - Output is built to 'dist/' directory (see package.json 'build' script).
// - Update 'base' if deploying to a subdirectory (e.g., '/vacation-planner').
