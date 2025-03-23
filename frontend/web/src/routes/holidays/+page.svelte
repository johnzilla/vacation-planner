<script>
  import { onMount } from 'svelte';
  let employers = [];
  let selectedEmployer = null;
  let holiday = { date: '', name: '', year: 2025 };

  onMount(async () => {
    const res = await fetch('/api/employers');
    employers = await res.json();
    selectedEmployer = employers[0]?.id;
  });

  async function submitHoliday() {
    const res = await fetch('/api/holidays', {
      method: 'POST',
      body: JSON.stringify({ ...holiday, employer_id: selectedEmployer }),
      headers: { 'Content-Type': 'application/json' },
    });
    if (res.ok) alert('Holiday added!');
  }
</script>

<main>
  <h1>Add Employer Holiday</h1>
  <select bind:value={selectedEmployer}>
    {#each employers as employer}
      <option value={employer.id}>{employer.name}</option>
    {/each}
  </select>
  <input type="date" bind:value={holiday.date} />
  <input type="text" bind:value={holiday.name} placeholder="Holiday Name" />
  <button on:click={submitHoliday}>Add Holiday</button>
</main>
