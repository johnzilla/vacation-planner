<script>
  import { onMount } from 'svelte';
  import { createSavedPlan } from '$lib/api';
  import { isAuthenticated, user } from '$lib/auth';
  
  // Get data from the page load function
  export let data;
  
  let suggestions = data.suggestions || [];
  let noSingleDays = true;
  let maxVacations = null;
  let warning = data.warning || null;
  let userId = 1;
  
  // For saving plans
  let showSaveModal = false;
  let planName = '';
  let isPublic = false;
  let saving = false;
  let saveError = null;
  let saveSuccess = false;
  
  // Use authenticated user's ID if available
  $: if ($isAuthenticated && $user) {
    userId = $user.id;
  }

  async function fetchSuggestions() {
    try {
      const params = new URLSearchParams({
        user_id: userId,
        no_single_days: noSingleDays,
        ...(maxVacations && { max_vacations: maxVacations })
      });
      const res = await fetch(`/api/suggestions?${params}`);
      const result = await res.json();
      suggestions = result.schedule || [];
      warning = result.warning;
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      warning = 'Failed to load suggestions. Please try again later.';
    }
  }
  
  function openSaveModal() {
    if (!$isAuthenticated) {
      // Redirect to login if not authenticated
      window.location.href = '/auth?redirect=/suggestions';
      return;
    }
    
    // Generate a default name based on the current date
    const today = new Date();
    planName = `Vacation Plan - ${today.toLocaleDateString()}`;
    showSaveModal = true;
    saveError = null;
    saveSuccess = false;
  }
  
  function closeSaveModal() {
    showSaveModal = false;
  }
  
  async function savePlan() {
    if (!planName.trim()) {
      saveError = "Please enter a name for your plan";
      return;
    }
    
    try {
      saving = true;
      saveError = null;
      
      // Prepare the schedule data
      const scheduleData = {
        periods: suggestions.map(s => ({
          start_date: s.start,
          end_date: s.end,
          days_used: s.days_used,
          total_days_off: s.total_days_off,
          efficiency: s.efficiency,
          breakdown: s.breakdown,
          explanation: s.explanation
        })),
        total_days_used: suggestions.reduce((sum, s) => sum + s.days_used, 0),
        total_days_off: suggestions.reduce((sum, s) => sum + s.total_days_off, 0),
        efficiency: suggestions.length > 0 
          ? suggestions.reduce((sum, s) => sum + s.total_days_off, 0) / 
            suggestions.reduce((sum, s) => sum + s.days_used, 0)
          : 0
      };
      
      // Create the plan
      const planData = {
        name: planName,
        year: new Date().getFullYear(),
        schedule: scheduleData,
        is_public: isPublic ? 1 : 0
      };
      
      await createSavedPlan(planData);
      saveSuccess = true;
      
      // Reset form after successful save
      setTimeout(() => {
        if (saveSuccess) {
          closeSaveModal();
        }
      }, 2000);
      
    } catch (err) {
      saveError = err.message || "Failed to save plan";
    } finally {
      saving = false;
    }
  }

  onMount(() => {
    fetchSuggestions();
    
    // Set up event listeners for filter changes
    const handleFilterChange = () => {
      fetchSuggestions();
    };
    
    // Watch for changes to filters
    const unsubscribe = () => {
      // This is just a placeholder for cleanup if needed
    };
    
    return unsubscribe;
  });
</script>

<svelte:head>
  <title>Vacation Suggestions | Vacation Planner</title>
</svelte:head>

<div class="suggestions-container">
  <h1>Vacation Schedule Suggestions</h1>
  
  <div class="filters">
    <div class="filter-group">
      <label class="checkbox-label">
        <input type="checkbox" bind:checked={noSingleDays} on:change={fetchSuggestions} />
        <span>No single days off (minimum 2 days)</span>
      </label>
    </div>
    
    <div class="filter-group">
      <label>
        Max Vacations:
        <input type="number" bind:value={maxVacations} min="1" placeholder="Unlimited" class="number-input" on:change={fetchSuggestions} />
      </label>
    </div>
  </div>
  
  {#if suggestions.length === 0}
    <div class="no-results">
      <p>No vacation suggestions available. Try adjusting your filters or time budget.</p>
    </div>
  {:else}
    <div class="save-button-container">
      <button class="save-button" on:click={openSaveModal}>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
          <polyline points="17 21 17 13 7 13 7 21"></polyline>
          <polyline points="7 3 7 8 15 8"></polyline>
        </svg>
        Save This Plan
      </button>
    </div>
    
    <div class="suggestions-list">
      {#each suggestions as suggestion, index}
        <div class="suggestion-card">
          <div class="suggestion-header">
            <h3>Vacation #{index + 1}</h3>
            <span class="days-badge">{suggestion.days_used} days</span>
          </div>
          
          <div class="suggestion-dates">
            <div class="date-range">
              <span class="date-label">From:</span>
              <span class="date-value">{suggestion.start}</span>
            </div>
            <div class="date-range">
              <span class="date-label">To:</span>
              <span class="date-value">{suggestion.end}</span>
            </div>
          </div>
          
          <div class="suggestion-stats">
            <div class="stat">
              <span class="stat-label">Days Used:</span>
              <span class="stat-value">{suggestion.days_used}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Total Days Off:</span>
              <span class="stat-value">{suggestion.total_days_off}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Efficiency:</span>
              <span class="stat-value">{suggestion.efficiency.toFixed(2)}</span>
            </div>
          </div>
          
          <div class="suggestion-breakdown">
            <div class="breakdown-item">
              <span class="breakdown-label">Workdays:</span>
              <span class="breakdown-value">{suggestion.breakdown.workdays}</span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label">Holidays:</span>
              <span class="breakdown-value">{suggestion.breakdown.holidays}</span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label">Weekends:</span>
              <span class="breakdown-value">{suggestion.breakdown.weekends}</span>
            </div>
          </div>
          
          <div class="suggestion-explanation">
            <p>{suggestion.explanation}</p>
          </div>
        </div>
      {/each}
    </div>
    
    <div class="suggestions-summary">
      <div class="summary-item">
        <span class="summary-label">Total Days Used:</span>
        <span class="summary-value">{suggestions.reduce((sum, s) => sum + s.days_used, 0)}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Total Days Off:</span>
        <span class="summary-value">{suggestions.reduce((sum, s) => sum + s.total_days_off, 0)}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Overall Efficiency:</span>
        <span class="summary-value">
          {(suggestions.reduce((sum, s) => sum + s.total_days_off, 0) / 
            suggestions.reduce((sum, s) => sum + s.days_used, 0)).toFixed(2)}
        </span>
      </div>
    </div>
  {/if}
  
  {#if warning}
    <div class="warning-message">
      <p>{warning}</p>
    </div>
  {/if}
</div>

{#if showSaveModal}
  <div class="modal-overlay">
    <div class="modal">
      <div class="modal-header">
        <h2>Save Vacation Plan</h2>
        <button class="close-btn" on:click={closeSaveModal}>&times;</button>
      </div>
      
      <div class="modal-content">
        {#if saveSuccess}
          <div class="success-message">
            <p>Your vacation plan has been saved successfully!</p>
            <p>You can view and manage your saved plans in the "My Plans" section.</p>
          </div>
        {:else}
          {#if saveError}
            <div class="error-message">
              <p>{saveError}</p>
            </div>
          {/if}
          
          <form on:submit|preventDefault={savePlan}>
            <div class="form-group">
              <label for="planName">Plan Name</label>
              <input 
                type="text" 
                id="planName" 
                bind:value={planName} 
                required 
                disabled={saving}
                placeholder="Enter a name for your plan"
              />
            </div>
            
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" bind:checked={isPublic} disabled={saving} />
                <span>Make this plan public (can be shared)</span>
              </label>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-secondary" on:click={closeSaveModal} disabled={saving}>
                Cancel
              </button>
              <button type="submit" class="btn-primary" disabled={saving}>
                {#if saving}
                  Saving...
                {:else}
                  Save Plan
                {/if}
              </button>
            </div>
          </form>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .suggestions-container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 2rem;
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .filter-group {
    display: flex;
    align-items: center;
  }
  
  .checkbox-label {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  
  .checkbox-label input {
    margin-right: 0.5rem;
  }
  
  .number-input {
    width: 80px;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-left: 0.5rem;
  }
  
  .save-button-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
  }
  
  .save-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: #4361ee;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }
  
  .save-button:hover {
    background-color: #3a56d4;
  }
  
  .suggestions-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .suggestion-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
  }
  
  .suggestion-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .suggestion-header h3 {
    margin: 0;
    color: #333;
  }
  
  .days-badge {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .suggestion-dates {
    display: flex;
    gap: 2rem;
    margin-bottom: 1rem;
  }
  
  .date-range {
    display: flex;
    flex-direction: column;
  }
  
  .date-label {
    font-size: 0.875rem;
    color: #666;
  }
  
  .date-value {
    font-weight: 500;
  }
  
  .suggestion-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
  }
  
  .stat {
    display: flex;
    flex-direction: column;
  }
  
  .stat-label {
    font-size: 0.875rem;
    color: #666;
  }
  
  .stat-value {
    font-weight: 500;
    color: #4361ee;
  }
  
  .suggestion-breakdown {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .breakdown-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .breakdown-label {
    font-size: 0.875rem;
    color: #666;
  }
  
  .breakdown-value {
    font-weight: 500;
  }
  
  .suggestion-explanation {
    font-style: italic;
    color: #666;
    font-size: 0.875rem;
  }
  
  .suggestions-summary {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
  }
</style>
    