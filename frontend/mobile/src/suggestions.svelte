<script>
  import { onMount } from 'svelte';
  let suggestions = [];
  let noSingleDays = true;
  let maxVacations = null;
  let warning = null;
  const userId = 1;

  async function fetchSuggestions() {
    const params = new URLSearchParams({
      user_id: userId,
      no_single_days: noSingleDays,
      ...(maxVacations && { max_vacations: maxVacations })
    });
    const res = await fetch(`/api/suggestions?${params}`);
    const result = await res.json();
    suggestions = result.schedule;
    warning = result.warning;
  }

  onMount(fetchSuggestions);
  $: noSingleDays, maxVacations, fetchSuggestions();
</script>

<main>
  <h1>Vacation Schedule</h1>
  <label>
    <input type="checkbox" bind:checked={noSingleDays} />
    No single days off (minimum 2 days)
  </label>
  <label>
    Max Vacations:
    <input type="number" bind:value={maxVacations} min="1" placeholder="Unlimited" />
  </label>
  {#each suggestions as s}
    <div>
      <p>{s.start} to {s.end}</p>
      <p>Days Used: {s.days_used}, Total Days Off: {s.total_days_off}, Efficiency: {s.efficiency.toFixed(2)}</p>
      <p>workdays: {s.breakdown.workdays}  holidays: {s.breakdown.holidays}  weekends: {s.breakdown.weekends}</p>
      <p>({s.explanation})</p>
    </div>
  {/each}
  <p>Total Days Used: {suggestions.reduce((sum, s) => sum + s.days_used, 0)}, Total Days Off: {suggestions.reduce((sum, s) => sum + s.total_days_off, 0)}</p>
  {#if warning}
    <p style="color: red">{warning}</p>
  {/if}
</main>
