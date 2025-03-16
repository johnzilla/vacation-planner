<script>
  import { onMount } from 'svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import { initAuth } from '$lib/auth';
  
  // Initialize authentication on app load
  onMount(() => {
    initAuth();
  });
</script>

<Navbar />

<main>
  <slot />
</main>

<footer>
  <div class="footer-content">
    <p>&copy; {new Date().getFullYear()} Vacation Planner</p>
  </div>
</footer>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #f9f9f9;
    color: #333;
    line-height: 1.6;
  }
  
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    min-height: calc(100vh - 180px); /* Account for header and footer */
  }
  
  footer {
    background-color: #f1f1f1;
    padding: 1.5rem 0;
    text-align: center;
    color: #666;
  }
  
  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }
</style> 