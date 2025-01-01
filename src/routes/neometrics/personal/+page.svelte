<!-- PersonalMetrics.svelte -->
<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let personalData;
  let taskChartCanvas;
  let timeChartCanvas;
  let completionRateCanvas;
  let taskTimeCanvas;

  async function loadData() {
    try {
      const response = await fetch('/assets/personal.json');
      personalData = await response.json();
      initializeCharts();
    } catch (error) {
      console.error('Error loading personal data:', error);
    }
  }
  let buttonText = 'AI Suggestions';
  let displayedImprovementAreas = personalData?.performanceMetrics.improvementAreas || [];

  async function fetchAISuggestions() {
    buttonText = 'Generating...';
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulate fetch delay
    displayedImprovementAreas = personalData?.performanceMetrics.improvementAreas || [];
    buttonText = 'AI Suggestions';
  }

  function initializeCharts() {
    // Task Completion Pie Chart
    new Chart(taskChartCanvas, {
      type: 'pie',
      data: {
        labels: ['Completed Tasks', 'Pending Tasks'],
        datasets: [{
          data: [
            personalData.personalTaskSummary.tasksCompleted,
            personalData.personalTaskSummary.pendingTasks
          ],
          backgroundColor: ['#00BFA5', '#FF6B6B'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: {
                family: "'Open Sans', sans-serif",
                size: 14,
                weight: 600
              }
            }
          },
          title: {
            display: true,
            text: 'Task Completion Overview',
            font: {
              family: "'Open Sans', sans-serif",
              size: 18,
              weight: 700
            }
          }
        }
      }
    });

    // Time Distribution Donut Chart
    new Chart(timeChartCanvas, {
      type: 'doughnut',
      data: {
        labels: ['Regular Hours', 'Overtime', 'Idle Time'],
        datasets: [{
          data: [
            personalData.timeTrackingInsights.totalHoursWorked - 
            personalData.timeTrackingInsights.overtime - 
            personalData.timeTrackingInsights.idleTime,
            personalData.timeTrackingInsights.overtime,
            personalData.timeTrackingInsights.idleTime
          ],
          backgroundColor: ['#4A90E2', '#9B59B6', '#F1C40F'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: {
                family: "'Open Sans', sans-serif",
                size: 14,
                weight: 600
              }
            }
          },
          title: {
            display: true,
            text: 'Time Distribution',
            font: {
              family: "'Open Sans', sans-serif",
              size: 18,
              weight: 700
            }
          }
        }
      }
    });

    // Task Time Analysis Bar Chart
    new Chart(taskTimeCanvas, {
      type: 'bar',
      data: {
        labels: ['Average', 'Target'],
        datasets: [{
          label: 'Task Time (Hours)',
          data: [
            personalData.timeTrackingInsights.averageTaskTime,
            2.0 // Example target time
          ],
          backgroundColor: ['#6C5CE7', '#A8A8A8'],
          borderRadius: 8,
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Task Time Analysis',
            font: {
              family: "'Open Sans', sans-serif",
              size: 18,
              weight: 700
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              display: true,
              color: '#E0E0E0'
            },
            ticks: {
              font: {
                family: "'Open Sans', sans-serif",
                size: 12,
                weight: 600
              }
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: {
                family: "'Open Sans', sans-serif",
                size: 12,
                weight: 600
              }
            }
          }
        }
      }
    });

    // Completion Rate Progress Bar (replacing gauge chart)
    const completionRate = personalData.performanceMetrics.completionRate;
    new Chart(completionRateCanvas, {
      type: 'bar',
      data: {
        labels: ['Completion Rate'],
        datasets: [{
          data: [completionRate],
          backgroundColor: getCompletionRateColor(completionRate),
          borderRadius: 8,
          borderWidth: 0
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Completion Rate',
            font: {
              family: "'Open Sans', sans-serif",
              size: 18,
              weight: 700
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            max: 100,
            grid: {
              display: false
            },
            ticks: {
              callback: function(value) {
                return value + '%';
              },
              font: {
                family: "'Open Sans', sans-serif",
                size: 12,
                weight: 600
              }
            }
          },
          y: {
            display: false
          }
        }
      }
    });
  }

  function getCompletionRateColor(rate) {
    if (rate >= 80) return '#00BFA5';
    if (rate >= 60) return '#FFA726';
    return '#FF6B6B';
  }

  onMount(() => {
    loadData();
  });
</script>

<svelte:head>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="content-wrapper">
  <div>
    <img src="/assets/neothink1.png" alt="Neothink Logo" class="neothink-logo" />
  </div>

  <div class="dashboard">
    <img src="/assets/neometrics1.png" alt="Neometrics Logo" class="neometrics-logo">
    <h1 class="dashboard-title">Performance Dashboard - {personalData?.name}</h1>
    
    <div class="metrics-grid">
      <div class="chart-card">
        <canvas bind:this={taskChartCanvas}></canvas>
      </div>

      <div class="chart-card">
        <canvas bind:this={timeChartCanvas}></canvas>
      </div>

      <div class="chart-card completion-rate">
        <canvas bind:this={completionRateCanvas}></canvas>
        <div class="completion-rate-label">
          {personalData?.performanceMetrics.completionRate}%
        </div>
      </div>

      <div class="chart-card">
        <canvas bind:this={taskTimeCanvas}></canvas>
      </div>

      <div class="info-card achievements">
        <h2>Top Achievements</h2>
        <ul>
          {#each personalData?.performanceMetrics.topAchievements || [] as achievement}
            <li>{achievement}</li>
          {/each}
        </ul>
      </div>

      <div class="info-card improvements">
        <h2>Areas for Improvement</h2>
        <button class="ai-suggestions-button" on:click={fetchAISuggestions}>
          {buttonText}
        </button>
        <ul>
          {#each displayedImprovementAreas as area}
            <li>{area}</li>
          {/each}
        </ul>
      </div>
    </div>
  </div>
</div>

<style>
  :global(html, body) {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow-y: auto; /* Ensure vertical scrolling */
  }

  :global(body) {
    background-color: #F5F7FA;
    font-family: 'Open Sans', sans-serif;
    overflow-y: scroll; /* Enable vertical scrolling */
  }

  .content-wrapper {
    height: 100%;
    overflow-y: auto; /* Ensure the content can scroll */
  }

  .dashboard {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
    position: relative;
  }

  .neothink-logo {
    position: absolute;
    top: 6px;
    left: 20px;
    width: 200px;
    height: auto;
  }

  .neometrics-logo {
    position: absolute;
    top: 1px;
    left: 65px;
    width: 230px;
    height: auto;
  }

  .dashboard-title {
    color: #2D3748;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Adjusted min-width */
    margin-left: 70px;
    gap: 1.5rem; /* Adjusted gap */
    margin-top: 2rem;
  }

  .chart-card {
    background: white;
    padding: 0.75rem; /* Adjusted padding */
    border-radius: 12px;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .chart-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }

  .info-card {
    background: white;
    padding: 1.5rem; /* Adjusted padding */
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }

  .completion-rate {
    position: relative;
  }

  .completion-rate-label {
    position: absolute;
    top: 70%; /* Moved down */
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 2rem;
    font-weight: 700;
    color: #2D3748;
  }

  h2 {
    color: #2D3748;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    padding: 1rem;
    margin-bottom: 0.5rem;
    background: #F8FAFC;
    border-radius: 8px;
    color: #4A5568;
    font-size: 1rem;
    line-height: 1.5;
  }

  li:last-child {
    margin-bottom: 0;
  }

  @media (max-width: 768px) {
    .dashboard {
      padding: 1rem;
    }

    .metrics-grid {
      grid-template-columns: 1fr;
    }

    .dashboard-title {
      font-size: 2rem;
    }
  }

  .ai-suggestions-button {
    display: inline-block;
    margin-bottom: 1rem;
    padding: 0.75rem 1.5rem;
    background-color: #4CAF50; /* Green */
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .ai-suggestions-button:hover {
    background-color: #45A049; /* Darker green */
  }

  .ai-suggestions-button:focus {
    outline: none;
  }
</style>

