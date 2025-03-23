<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { login, register, isAuthenticated, authError } from '$lib/auth';

  let email = '';
  let password = '';
  let confirmPassword = '';
  let isLogin = true; // Toggle between login and register forms
  let loading = false;
  let error = '';

  // Subscribe to auth error store
  $: if ($authError) {
    error = $authError;
  }

  // Redirect if already authenticated
  onMount(() => {
    if ($isAuthenticated) {
      goto('/');
    }
  });

  // Handle form submission
  async function handleSubmit() {
    error = '';
    loading = true;

    if (!isLogin && password !== confirmPassword) {
      error = 'Passwords do not match';
      loading = false;
      return;
    }

    try {
      let result;

      if (isLogin) {
        result = await login(email, password);
      } else {
        result = await register(email, password);
      }

      if (result.success) {
        goto('/');
      } else {
        error = result.error || 'Authentication failed';
      }
    } catch (err) {
      error = err.message || 'An unexpected error occurred';
    } finally {
      loading = false;
    }
  }

  // Toggle between login and register forms
  function toggleForm() {
    isLogin = !isLogin;
    error = '';
  }
</script>

<svelte:head>
  <title>{isLogin ? 'Login' : 'Register'} | Vacation Planner</title>
</svelte:head>

<div class="auth-container">
  <div class="auth-card">
    <h1>{isLogin ? 'Login' : 'Create Account'}</h1>

    <p class="auth-subtitle">
      {#if isLogin}
        Sign in to save and share your vacation plans
      {:else}
        Create an account to save and share your vacation plans
      {/if}
    </p>

    {#if error}
      <div class="error-message">
        {error}
      </div>
    {/if}

    <form on:submit|preventDefault={handleSubmit}>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          bind:value={email}
          required
          disabled={loading}
          placeholder="your@email.com"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          bind:value={password}
          required
          disabled={loading}
          placeholder="••••••••"
        />
      </div>

      {#if !isLogin}
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            bind:value={confirmPassword}
            required
            disabled={loading}
            placeholder="••••••••"
          />
        </div>
      {/if}

      <button type="submit" class="btn-primary" disabled={loading}>
        {#if loading}
          Loading...
        {:else if isLogin}
          Login
        {:else}
          Register
        {/if}
      </button>
    </form>

    <div class="auth-footer">
      {#if isLogin}
        <p>
          Don't have an account? <button class="link-button" on:click={toggleForm}>Register</button>
        </p>
      {:else}
        <p>
          Already have an account? <button class="link-button" on:click={toggleForm}>Login</button>
        </p>
      {/if}
    </div>

    <div class="guest-option">
      <p>Or <a href="/">continue as guest</a> (limited features)</p>
    </div>
  </div>
</div>

<style>
  .auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    padding: 2rem;
  }

  .auth-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    width: 100%;
    max-width: 400px;
  }

  h1 {
    margin-top: 0;
    color: #2a2a2a;
    text-align: center;
  }

  .auth-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 1.5rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  .btn-primary {
    width: 100%;
    padding: 0.75rem;
    background-color: #4361ee;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 1rem;
  }

  .btn-primary:hover {
    background-color: #3a56d4;
  }

  .btn-primary:disabled {
    background-color: #a0a0a0;
    cursor: not-allowed;
  }

  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1rem;
  }

  .auth-footer {
    margin-top: 1.5rem;
    text-align: center;
  }

  .link-button {
    background: none;
    border: none;
    color: #4361ee;
    cursor: pointer;
    font-size: inherit;
    padding: 0;
    text-decoration: underline;
  }

  .guest-option {
    margin-top: 1.5rem;
    text-align: center;
    padding-top: 1rem;
    border-top: 1px solid #eee;
  }

  .guest-option a {
    color: #4361ee;
    text-decoration: none;
  }

  .guest-option a:hover {
    text-decoration: underline;
  }
</style>
