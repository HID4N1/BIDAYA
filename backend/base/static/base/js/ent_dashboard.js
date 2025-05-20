google.charts.load('current', { packages: ['corechart'] });
google.charts.setOnLoadCallback(() => {
    if (typeof google.visualization === 'undefined') {
        console.error('Google Charts library failed to load.');
        return;
    }
    console.log('Google Charts library loaded successfully.');
    drawCharts();
});

// Store chart references and data globally for resize handling
let fundingOverviewChart, projectSuccessChart;
let fundingOverviewDataTable, projectSuccessDataTable;
let fundingOverviewOptions, projectSuccessOptions;

function drawCharts() {
    try {
        // Parse JSON data embedded in the HTML
        const fundingLabels = JSON.parse(document.getElementById('fundingLabels').textContent);
        const fundingData = JSON.parse(document.getElementById('fundingData').textContent);

        console.log('Funding Labels:', fundingLabels);
        console.log('Funding Data:', fundingData);

        // Prepare data for funding overview chart
        const fundingOverviewDataArray = [['Project', 'Amount']];
        for (let i = 0; i < fundingLabels.length; i++) {
            fundingOverviewDataArray.push([fundingLabels[i], fundingData[i]]);
        }
        console.log('Funding Overview Data Array:', fundingOverviewDataArray);

        fundingOverviewDataTable = google.visualization.arrayToDataTable(fundingOverviewDataArray);

        fundingOverviewOptions = {
            title: 'Funding Overview',
            legend: { position: 'none' },
            hAxis: { title: 'Projects' },
            vAxis: { title: 'Amount', minValue: 0 },
            chartArea: { width: '70%', height: '70%' },
        };

        fundingOverviewChart = new google.visualization.ColumnChart(document.getElementById('fundingOverviewChart'));
        fundingOverviewChart.draw(fundingOverviewDataTable, fundingOverviewOptions);

        console.log('Funding Overview Chart rendered successfully.');

        // Prepare data for project success chart
        const fundedCount = parseInt(document.getElementById('fundedCount')?.textContent || 0);
        const inProgressCount = parseInt(document.getElementById('inProgressCount')?.textContent || 0);
        const notFundedCount = parseInt(document.getElementById('notFundedCount')?.textContent || 0);

        projectSuccessDataTable = google.visualization.arrayToDataTable([
            ['Status', 'Count'],
            ['Funded', fundedCount],
            ['In Progress', inProgressCount],
            ['Not Funded', notFundedCount],
        ]);

        projectSuccessOptions = {
            title: 'Project Success',
            pieHole: 0.4,
            legend: { position: 'bottom' },
            chartArea: { width: '70%', height: '70%' },
            colors: ['#4CAF50', '#FFC107', '#F44336'] // Green, Yellow, Red
        };

        projectSuccessChart = new google.visualization.PieChart(document.getElementById('projectSuccessChart'));
        projectSuccessChart.draw(projectSuccessDataTable, projectSuccessOptions);

        console.log('Project Success Chart rendered successfully.');

    } catch (error) {
        console.error('Error drawing charts:', error);
    }
}

// Add debounced resize event listener
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        if (fundingOverviewChart && fundingOverviewDataTable && fundingOverviewOptions) {
            fundingOverviewChart.draw(fundingOverviewDataTable, fundingOverviewOptions);
        }
        if (projectSuccessChart && projectSuccessDataTable && projectSuccessOptions) {
            projectSuccessChart.draw(projectSuccessDataTable, projectSuccessOptions);
        }
    }, 250);
});