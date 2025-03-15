// frontend/web/svelte.config.js
// Configuration for SvelteKit to build the Vacation Planner web app.

import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({
      // Default options for static builds
      pages: 'dist',
      assets: 'dist',
      fallback: undefined,
      precompress: false
    }),
    paths: {
      base: '' // Set to '/your-base-path' if deploying to a subdirectory
    }
  }
};

export default config;

// Notes:
// - Uses '@sveltejs/adapter-static' to generate a static site for Vercel or similar hosting.
// - Output is built to 'dist/' directory (see package.json 'build' script).
// - Update 'base' if deploying to a subdirectory (e.g., '/vacation-planner').
// - Switch to 'adapter-auto' or another adapter if SSR or serverless is needed.
// - Add custom Vite config (e.g., plugins) inside 'kit' if required.
