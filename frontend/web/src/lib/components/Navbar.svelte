<script>
  import { isAuthenticated, user, logout } from '$lib/auth';
  import { onMount } from 'svelte';

  // Initialize auth on component mount
  onMount(() => {
    // Check if token exists in localStorage and update stores
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (token && userData) {
      isAuthenticated.set(true);
      user.set(JSON.parse(userData));
    }
  });

  function handleLogout() {
    logout();
    window.location.href = '/'; // Redirect to home page
  }
</script>

<nav>
  <div class="nav-container">
    <div class="logo">
      <a href="/">Vacation Planner</a>
    </div>

    <div class="nav-links">
      <a href="/" class="nav-link">Home</a>
      <a href="/time-budget" class="nav-link">Time Budget</a>
      <a href="/holidays" class="nav-link">Holidays</a>
      <a href="/suggestions" class="nav-link">Suggestions</a>

      {#if $isAuthenticated}
        <a href="/saved-plans" class="nav-link">My Plans</a>
      {/if}
    </div>

    <div class="auth-section">
      {#if $isAuthenticated}
        <div class="user-info">
          <span>Hello, {$user?.email}</span>
          <button on:click={handleLogout} class="logout-btn">Logout</button>
        </div>
      {:else}
        <a href="/auth" class="login-btn">Login</a>
      {/if}
    </div>
  </div>
</nav>

<style>
  nav {
    background-color: #4361ee;
    color: white;
    padding: 1rem 0;
  }

  .nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .logo a {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
  }

  .nav-links {
    display: flex;
    gap: 1.5rem;
  }

  .nav-link {
    color: white;
    text-decoration: none;
    font-weight: 500;
  }

  .nav-link:hover {
    text-decoration: underline;
  }

  .auth-section {
    display: flex;
    align-items: center;
  }

  .login-btn {
    background-color: white;
    color: #4361ee;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .logout-btn {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
  }

  .logout-btn:hover {
    background-color: rgba(255, 255, 255, 0.3);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .nav-container {
      flex-direction: column;
      gap: 1rem;
    }

    .nav-links {
      flex-wrap: wrap;
      justify-content: center;
    }
  }
</style>
