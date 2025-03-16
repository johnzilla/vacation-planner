<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { getSharedPlan } from '$lib/api';
  
  let plan = null;
  let loading = true;
  let error = null;
  
  onMount(async () => {
    await loadSharedPlan();
  });
  
  async function loadSharedPlan() {
    try {
      loading = true;
      error = null;
      
      const token = $page.params.token;
      plan = await getSharedPlan(token);
    } catch (err) {
      error = err.message || 'Failed to load shared plan';
    } finally {
      loading = false;
    }
  }
  
  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  }
</script>

<svelte:head>
  <title>{plan ? `${plan.name} - Shared Plan` : 'Shared Plan'} | Vacation Planner</title>
</svelte:head>

<div class="shared-plan-container">
  {#if loading}
    <div class="loading">Loading shared plan...</div>
  {:else if error}
    <div class="error-message">
      <h2>Error Loading Plan</h2>
      <p>{error}</p>
      <p>The plan may have been deleted or the link is invalid.</p>
      <a href="/" class="btn-primary">Go to Home</a>
    </div>
  {:else if plan}
    <div class="shared-plan-header">
      <h1>{plan.name}</h1>
      <div class="plan-meta">
        <span class="year-badge">{plan.year}</span>
        <span class="shared-badge">Shared Plan</span>
      </div>
    </div>
    
    <div class="plan-details">
      <p>Created: {formatDate(plan.created_at)}</p>
    </div>
    
    <div class="vacation-schedule">
      <h2>Vacation Schedule</h2>
      
      {#if plan.schedule && plan.schedule.periods && plan.schedule.periods.length > 0}
        <div class="schedule-list">
          {#each plan.schedule.periods as period, index}
            <div class="vacation-period">
              <div class="period-header">
                <h3>Vacation #{index + 1}</h3>
                <span class="days-badge">{period.days_used} days</span>
              </div>
              
              <div class="period-dates">
                <div class="date-range">
                  <span class="date-label">From:</span>
                  <span class="date-value">{formatDate(period.start_date)}</span>
                </div>
                <div class="date-range">
                  <span class="date-label">To:</span>
                  <span class="date-value">{formatDate(period.end_date)}</span>
                </div>
              </div>
              
              <div class="period-stats">
                <div class="stat">
                  <span class="stat-label">Total Days Off:</span>
                  <span class="stat-value">{period.total_days_off}</span>
                </div>
                <div class="stat">
                  <span class="stat-label">Efficiency:</span>
                  <span class="stat-value">{period.efficiency.toFixed(2)}</span>
                </div>
              </div>
            </div>
          {/each}
        </div>
        
        <div class="schedule-summary">
          <div class="summary-item">
            <span class="summary-label">Total Vacation Days Used:</span>
            <span class="summary-value">{plan.schedule.total_days_used}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Total Days Off (including weekends/holidays):</span>
            <span class="summary-value">{plan.schedule.total_days_off}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Overall Efficiency:</span>
            <span class="summary-value">{plan.schedule.efficiency?.toFixed(2) || 'N/A'}</span>
          </div>
        </div>
      {:else}
        <p class="no-schedule">This plan doesn't contain any vacation periods.</p>
      {/if}
    </div>
    
    <div class="action-buttons">
      <a href="/" class="btn-primary">Go to Home</a>
      <a href="/auth" class="btn-secondary">Login to Create Your Own Plan</a>
    </div>
  {/if}
</div>

<style>
  .shared-plan-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  .loading {
    text-align: center;
    padding: 3rem 1rem;
    color: #666;
  }
  
  .error-message {
    text-align: center;
    padding: 3rem 1rem;
    background-color: #f8f8f8;
    border-radius: 8px;
    margin: 2rem 0;
  }
  
  .error-message h2 {
    color: #c62828;
    margin-top: 0;
  }
  
  .shared-plan-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  
  .shared-plan-header h1 {
    margin: 0;
    color: #333;
  }
  
  .plan-meta {
    display: flex;
    gap: 0.5rem;
  }
  
  .year-badge, .shared-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .year-badge {
    background-color: #e0e7ff;
    color: #4361ee;
  }
  
  .shared-badge {
    background-color: #fff8e1;
    color: #ff8f00;
  }
  
  .plan-details {
    color: #666;
    margin-bottom: 2rem;
  }
  
  .vacation-schedule {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .vacation-schedule h2 {
    margin-top: 0;
    color: #333;
    margin-bottom: 1.5rem;
  }
  
  .schedule-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .vacation-period {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 1rem;
  }
  
  .period-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .period-header h3 {
    margin: 0;
    font-size: 1.1rem;
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
  
  .period-dates {
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
  
  .period-stats {
    display: flex;
    gap: 2rem;
    border-top: 1px solid #eee;
    padding-top: 1rem;
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
  
  .schedule-summary {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 2px solid #eee;
  }
  
  .summary-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .summary-label {
    color: #666;
  }
  
  .summary-value {
    font-weight: 500;
    color: #4361ee;
  }
  
  .no-schedule {
    text-align: center;
    padding: 2rem;
    color: #666;
    background-color: #f8f8f8;
    border-radius: 4px;
  }
  
  .action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .btn-primary, .btn-secondary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
    text-align: center;
  }
  
  .btn-primary {
    background-color: #4361ee;
    color: white;
  }
  
  .btn-secondary {
    background-color: #f1f1f1;
    color: #333;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .shared-plan-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .period-dates, .period-stats {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .action-buttons {
      flex-direction: column;
    }
  }
</style> 