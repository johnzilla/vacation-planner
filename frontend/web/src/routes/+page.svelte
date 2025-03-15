<script>
  import { goto } from '$app/navigation';

  function navigateTo(path) {
    goto(path);
  }
</script>

<main>
  <h1>Welcome to Vacation Planner</h1>
  <p>Plan your time off efficiently with our AI-powered scheduler.</p>
  
  <div>
    <button on:click={() => navigateTo('/time-budget')}>Set Your Time Budget</button>
    <button on:click={() => navigateTo('/holidays')}>Add Employer Holidays</button>
    <button on:click={() => navigateTo('/suggestions')}>View Vacation Suggestions</button>
  </div>

  <p>Get started by setting your vacation time budget or adding employer holidays, then see your optimized schedule!</p>
</main>

<!-- Notes: -->
<!-- - This is a basic home page with navigation to other features. -->
<!-- - Customize styling (add <style> block) and content as needed. -->
<!-- - Consider adding a logo or introductory graphic in the future. -->
