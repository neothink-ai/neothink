<script>
  import Calendar from '../home/components/Calendar.svelte';
</script>

<div class="home-container">
  <div class="calendar-wrapper">
    <Calendar />
  </div>
</div>

<style>
  .home-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
    background-color: #f4f5f7;
    height: 100vh;
    width: 100vw;
  }

  .calendar-wrapper {
    width: 100%;
    height: 100%;
    max-width: 1200px; /* Optional: limit the max width */
    max-height: 800px; /* Optional: limit the max height */
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(9, 30, 66, 0.1);
    padding: 24px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }
</style>