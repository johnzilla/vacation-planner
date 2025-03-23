<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getSavedPlans, deleteSavedPlan, createShareLink } from '$lib/api';
  import { isAuthenticated } from '$lib/auth';

  let plans = [];
  let loading = true;
  let error = null;
  let shareUrl = '';
  let showShareModal = false;
  let selectedPlan = null;

  // Redirect if not authenticated
  $: if ($isAuthenticated === false) {
    goto('/auth');
  }

  onMount(async () => {
    if ($isAuthenticated) {
      await loadPlans();
    }
  });

  async function loadPlans() {
    try {
      loading = true;
      error = null;
      plans = await getSavedPlans();
    } catch (err) {
      error = err.message || 'Failed to load saved plans';
    } finally {
      loading = false;
    }
  }

  async function handleDelete(planId) {
    if (!confirm('Are you sure you want to delete this plan?')) {
      return;
    }

    try {
      loading = true;
      await deleteSavedPlan(planId);
      plans = plans.filter((plan) => plan.id !== planId);
    } catch (err) {
      error = err.message || 'Failed to delete plan';
    } finally {
      loading = false;
    }
  }

  async function handleShare(plan) {
    try {
      loading = true;
      selectedPlan = plan;

      // If plan doesn't have a share token, create one
      if (!plan.share_token) {
        const updatedPlan = await createShareLink(plan.id);
        plan.share_token = updatedPlan.share_token;

        // Update the plan in the list
        plans = plans.map((p) => (p.id === plan.id ? updatedPlan : p));
      }

      // Create shareable URL
      const baseUrl = window.location.origin;
      shareUrl = `${baseUrl}/shared/${plan.share_token}`;

      showShareModal = true;
    } catch (err) {
      error = err.message || 'Failed to create share link';
    } finally {
      loading = false;
    }
  }

  function closeShareModal() {
    showShareModal = false;
    shareUrl = '';
  }

  function copyShareLink() {
    navigator.clipboard
      .writeText(shareUrl)
      .then(() => {
        alert('Link copied to clipboard!');
      })
      .catch((err) => {
        console.error('Failed to copy link:', err);
      });
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  }
</script>

<svelte:head>
  <title>My Saved Plans | Vacation Planner</title>
</svelte:head>

<div class="saved-plans-container">
  <h1>My Saved Vacation Plans</h1>

  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}

  {#if loading}
    <div class="loading">Loading your plans...</div>
  {:else if plans.length === 0}
    <div class="empty-state">
      <p>You don't have any saved vacation plans yet.</p>
      <p>
        <a href="/suggestions" class="btn-primary">Create a vacation plan</a>
      </p>
    </div>
  {:else}
    <div class="plans-grid">
      {#each plans as plan}
        <div class="plan-card">
          <div class="plan-header">
            <h2>{plan.name}</h2>
            <span class="year-badge">{plan.year}</span>
          </div>

          <div class="plan-details">
            <p>Created: {formatDate(plan.created_at)}</p>
            <p>Status: {plan.is_public ? 'Public' : 'Private'}</p>
          </div>

          <div class="plan-actions">
            <a href={`/saved-plans/${plan.id}`} class="btn-view">View</a>
            <a href={`/saved-plans/${plan.id}/edit`} class="btn-edit">Edit</a>
            <button class="btn-share" on:click={() => handleShare(plan)}>Share</button>
            <button class="btn-delete" on:click={() => handleDelete(plan.id)}>Delete</button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

{#if showShareModal}
  <div class="modal-overlay">
    <div class="modal">
      <div class="modal-header">
        <h2>Share "{selectedPlan?.name}"</h2>
        <button class="close-btn" on:click={closeShareModal}>&times;</button>
      </div>

      <div class="modal-content">
        <p>Share this link with others to view your vacation plan:</p>

        <div class="share-link-container">
          <input type="text" readonly value={shareUrl} class="share-link-input" />
          <button class="copy-btn" on:click={copyShareLink}>Copy</button>
        </div>

        <p class="share-note">Note: Anyone with this link can view this vacation plan.</p>
      </div>
    </div>
  </div>
{/if}

<style>
  .saved-plans-container {
    max-width: 1000px;
    margin: 0 auto;
  }

  h1 {
    margin-bottom: 2rem;
    color: #333;
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #666;
  }

  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
  }

  .empty-state {
    text-align: center;
    padding: 3rem 1rem;
    background-color: #f5f5f5;
    border-radius: 8px;
    margin-top: 2rem;
  }

  .btn-primary {
    display: inline-block;
    background-color: #4361ee;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
    margin-top: 1rem;
  }

  .plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .plan-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    transition:
      transform 0.2s,
      box-shadow 0.2s;
  }

  .plan-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .plan-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .plan-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #333;
  }

  .year-badge {
    background-color: #e0e7ff;
    color: #4361ee;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .plan-details {
    margin-bottom: 1.5rem;
    color: #666;
  }

  .plan-details p {
    margin: 0.5rem 0;
    font-size: 0.875rem;
  }

  .plan-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }

  .btn-view,
  .btn-edit,
  .btn-share,
  .btn-delete {
    padding: 0.5rem;
    border-radius: 4px;
    text-align: center;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
  }

  .btn-view,
  .btn-edit {
    text-decoration: none;
  }

  .btn-view {
    background-color: #e0e7ff;
    color: #4361ee;
  }

  .btn-edit {
    background-color: #e0f2f1;
    color: #009688;
  }

  .btn-share {
    background-color: #e8f5e9;
    color: #2e7d32;
    border: none;
  }

  .btn-delete {
    background-color: #ffebee;
    color: #c62828;
    border: none;
  }

  /* Modal styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background-color: white;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #eee;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.25rem;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
  }

  .modal-content {
    padding: 1.5rem;
  }

  .share-link-container {
    display: flex;
    margin: 1rem 0;
  }

  .share-link-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
    font-size: 0.875rem;
  }

  .copy-btn {
    background-color: #4361ee;
    color: white;
    border: none;
    padding: 0 1rem;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
  }

  .share-note {
    font-size: 0.875rem;
    color: #666;
    margin-top: 1rem;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .plans-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
