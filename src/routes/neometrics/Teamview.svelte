<script>
    import { onMount } from "svelte";
    import { Chart } from "chart.js/auto";
    import ChartDataLabels from "chartjs-plugin-datalabels";

    Chart.register(ChartDataLabels);

    let teamData = {
        performanceSummary: {
            overallEfficiency: null,
            tasksCompleted: null,
            currentWorkload: null,
            topPerformer: {
                name: null,
                photo: "static/assets/hema.jpg",
                metrics: {
                    efficiency: null,
                    tasksCompleted: null
                }
            }
        }
    };

    let chartInstance;
    let isGaugeVisible = false;
    let isTopPerformerCardVisible = false;
    let imageError = false;

    const createChartConfig = (efficiency) => ({
        type: 'doughnut',
        data: {
            datasets: [{
                data: [efficiency, 100 - efficiency],
                backgroundColor: ['#00bf63', '#e0e0e0'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            rotation: -90,
            circumference: 180,
            cutout: '80%',
            animation: {
                duration: 1500,
                easing: 'easeInOutQuad',
            },
            plugins: {
                tooltip: {
                    enabled: false,
                },
                legend: {
                    display: false
                },
                datalabels: {
                    display: true,
                    formatter: (value, context) => {
                        if (context.dataIndex === 0) {
                            return `${value}%`;
                        }
                        return '';
                    },
                    color: '#333',
                    font: {
                        size: 24,
                        weight: 'bold'
                    },
                    align: 'center',
                    anchor: 'center'
                }
            },
        }
    });

    const showGaugeChart = (efficiency) => {
        if (!efficiency) return;
        
        isGaugeVisible = true;
        isTopPerformerCardVisible = false;
        
        setTimeout(() => {
            if (chartInstance) {
                chartInstance.destroy();
            }

            const ctx = document.getElementById("efficiencyGauge");
            if (ctx) {
                chartInstance = new Chart(ctx, createChartConfig(efficiency));
            }
        }, 0);
    };

    const showTopPerformerCard = () => {
        isTopPerformerCardVisible = true;
        isGaugeVisible = false;
        if (chartInstance) {
            chartInstance.destroy();
        }
    };

    const handleImageError = () => {
        imageError = true;
        console.error('Image failed to load. Using fallback avatar.');
    };

    onMount(async () => {
        try {
            const response = await fetch("/assets/team.json");
            if (!response.ok) {
                throw new Error("Failed to fetch team.json");
            }
            const data = await response.json();
            
            if (data.performanceSummary?.topPerformer) {
                data.performanceSummary.topPerformer.photo = "/assets/hema.jpg";
            }
            
            teamData = data;
        } catch (error) {
            console.error("Error fetching team data:", error);
        }
    });
</script>

<style>
    .metrics-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 16px;
        padding: 20px;
    }

    .metric-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 150px;
        height: 120px;
        margin: 8px;
        margin-top: 80px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 191, 99, 0.5);
        background-color: white;
        transition: transform 0.2s ease-in-out;
        cursor: pointer;
    }

    .metric-box:hover {
        transform: translateY(-5px);
    }

    .metric-title {
        font-size: 1rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
        text-align: center;
    }

    .metric-value {
        font-size: 1.5rem;
        color: #00bf63;
        text-align: center;
    }

    .metric-subtext {
        font-size: 0.875rem;
        color: #666;
        text-align: center;
    }

    .gauge-container {
        position: relative;
        height: 200px;
        width: 100%;
        max-width: 300px;
        margin: 20px auto;
        opacity: 1;
        transition: opacity 0.3s ease-in-out;
    }

    .gauge-container.hidden {
        display: none;
        opacity: 0;
    }

    .gauge-label {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 1rem;
        font-weight: bold;
        color: #333;
        text-align: center;
    }

    .top-performer-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #fff;
        box-shadow: 0px 4px 10px rgba(0, 191, 99, 0.5);
        border-radius: 12px;
        padding: 15px;
        width: 200px;
        margin: 15px auto;
        opacity: 1;
        transition: opacity 0.3s ease-in-out;
    }

    .top-performer-photo {
        border-radius: 50%;
        width: 60px;
        height: 60px;
        margin-bottom: 8px;
        border: 2px solid #00bf63;
        background-color: #e0e0e0;
        object-fit: cover;
    }

    .avatar-fallback {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #00bf63;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 8px;
    }

    .top-performer-name {
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
        text-align: center;
    }

    .top-performer-metrics {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
        line-height: 1.4;
    }

    @media (max-width: 768px) {
        .metric-box {
            width: 130px;
            height: 110px;
            margin-top: 10px;
        }

        .gauge-container {
            height: 180px;
            max-width: 250px;
        }

        .top-performer-card {
            width: 180px;
            padding: 12px;
        }
    }
</style>

<div class="metrics-container">
    <div class="metric-box" on:click={() => showGaugeChart(teamData.performanceSummary?.overallEfficiency)}>
        <div class="metric-title">Overall Efficiency</div>
        <div class="metric-value">{teamData.performanceSummary?.overallEfficiency ?? "Loading..."}%</div>
    </div>

    <div class="metric-box">
        <div class="metric-title">Tasks Completed</div>
        <div class="metric-value">{teamData.performanceSummary?.tasksCompleted ?? "Loading..."}</div>
    </div>

    <div class="metric-box">
        <div class="metric-title">Current Workload</div>
        <div class="metric-value">{teamData.performanceSummary?.currentWorkload ?? "Loading..."}</div>
    </div>

    <div class="metric-box" on:click={showTopPerformerCard}>
        <div class="metric-title">Top Performer</div>
        <div class="metric-value">
            {teamData.performanceSummary?.topPerformer?.name ?? "Loading..."}
        </div>
        <div class="metric-subtext">
            Efficiency: {teamData.performanceSummary?.topPerformer?.metrics?.efficiency ?? "N/A"}%<br />
            Tasks: {teamData.performanceSummary?.topPerformer?.metrics?.tasksCompleted ?? "N/A"}
        </div>
    </div>
</div>

{#if isGaugeVisible}
    <div class="gauge-container" class:hidden={!isGaugeVisible}>
        <canvas id="efficiencyGauge"></canvas>
        <div class="gauge-label">Overall Efficiency</div>
    </div>
{/if}

{#if isTopPerformerCardVisible}
    <div class="top-performer-card">
        {#if teamData.performanceSummary?.topPerformer?.photo && !imageError}
            <img 
                src={teamData.performanceSummary.topPerformer.photo}
                alt="Top Performer" 
                class="top-performer-photo"
                on:error={handleImageError}
            />
        {:else}
            <div class="avatar-fallback">
                {teamData.performanceSummary?.topPerformer?.name?.[0] ?? '?'}
            </div>
        {/if}
        <div class="top-performer-name">
            {teamData.performanceSummary?.topPerformer?.name ?? 'Loading...'}
        </div>
        <div class="top-performer-metrics">
            Efficiency: {teamData.performanceSummary?.topPerformer?.metrics?.efficiency ?? 'N/A'}%<br />
            Tasks: {teamData.performanceSummary?.topPerformer?.metrics?.tasksCompleted ?? 'N/A'}
        </div>
    </div>
{/if}