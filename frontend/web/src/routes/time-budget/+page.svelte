<script>
  import { onMount } from 'svelte';
  let accruedDays = 0;
  let usedDays = 0;
  let currentBudget = { accrued_days: 0, used_days: 0 };
  let errorMessage = '';

  const userId = 1;  // Mocked

  onMount(async () => {
    const res = await fetch(`/api/time-budget?user_id=${userId}`);
    currentBudget = await res.json();
    accruedDays = currentBudget.accrued_days;
    usedDays = currentBudget.used_days;
  });

  $: isValid = parseFloat(usedDays) <= parseFloat(accruedDays);
  $: errorMessage = isValid ? '' : 'Used days cannot exceed accrued days';

  async function updateBudget() {
    if (!isValid) return;
    const res = await fetch('/api/time-budget', {
      method: 'POST',
      body: JSON.stringify({ 
        accrued_days: parseFloat(accruedDays), 
        used_days: parseFloat(usedDays) 
      }),
      headers: { 'Content-Type': 'application/json' }
    });
    if (res.ok) {
      const updated = await res.json();
      currentBudget.accrued_days = updated.accrued_days;
      currentBudget.used_days = updated.used_days;
      alert('Time budget updated!');
    }
  }
</script>

<main>
  <h1>Your Vacation Time</h1>
  <p>Current Accrued: {currentBudget.accrued_days} days</p>
  <p>Current Used: {currentBudget.used_days} days</p>
  <input type="number" bind:value={accruedDays} step="0.5" min="0" placeholder="Accrued Days" />
  <input type="number" bind:value={usedDays} step="0.5" min="0" placeholder="Used Days" />
  {#if errorMessage}
    <p style="color: red">{errorMessage}</p>
  {/if}
  <button on:click={updateBudget} disabled={!isValid}>Update Time Budget</button>
</main>
