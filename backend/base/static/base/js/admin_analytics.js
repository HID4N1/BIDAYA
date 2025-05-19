document.addEventListener('DOMContentLoaded', function() {
    // User Growth Chart (Line Chart)
    const userGrowthCtx = document.getElementById('userGrowthChart').getContext('2d');
    new Chart(userGrowthCtx, {
        type: 'line',
        data: {
            labels: JSON.parse(document.getElementById('userGrowthData').textContent).map(item => item.date),
            datasets: [
                {
                    label: 'Entrepreneurs',
                    data: JSON.parse(document.getElementById('userGrowthData').textContent).map(item => item.entrepreneurs),
                    borderColor: '#4cc9f0',
                    backgroundColor: 'rgba(76, 201, 240, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Investors',
                    data: JSON.parse(document.getElementById('userGrowthData').textContent).map(item => item.investors),
                    borderColor: '#f8961e',
                    backgroundColor: 'rgba(248, 150, 30, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });

    // Revenue Sources Chart (Doughnut Chart)
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'doughnut',
        data: {
            labels: ['Investments', 'Donations'],
            datasets: [{
                data: [
                    parseFloat(document.getElementById('totalInvestment').getAttribute('data-value')),
                    parseFloat(document.getElementById('totalDonation').getAttribute('data-value'))
                ],
                backgroundColor: [
                    '#4361ee',
                    '#f72585'
                ],
                borderWidth: 1,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += '$' + context.raw.toLocaleString();
                            return label;
                        }
                    }
                }
            }
        }
    });

    // Project Status Chart (Bar Chart)
    const projectStatusCtx = document.getElementById('projectStatusChart').getContext('2d');
    new Chart(projectStatusCtx, {
        type: 'bar',
        data: {
            labels: ['Active', 'Completed', 'Pending'],
            datasets: [{
                label: 'Projects',
                data: [
                    parseInt(document.getElementById('activeProjects').textContent),
                    parseInt(document.getElementById('completedProjects').textContent),
                    parseInt(document.getElementById('pendingProjects').textContent)
                ],
                backgroundColor: [
                    '#4cc9f0',
                    '#7209b7',
                    '#f8961e'
                ],
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw + ' projects';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
});

    // Revenue Sources Chart
    const revenueData = JSON.parse('{{ revenue_sources|escapejs }}');
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    
    new Chart(revenueCtx, {
        type: 'doughnut',
        data: {
            labels: revenueData.map(item => item.source),
            datasets: [{
                data: revenueData.map(item => item.amount),
                backgroundColor: ['#4361ee', '#3f37c9']
            }]
        }
    });