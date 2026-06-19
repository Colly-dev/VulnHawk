// SecureAudit Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('SecureAudit Dashboard Loaded');
    
    // Initialize charts if they exist
    initializeCharts();
});

function initializeCharts() {
    // Fetch stats from API
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            createSeverityChart(data.severity_counts);
        })
        .catch(error => console.error('Error fetching stats:', error));
}

function createSeverityChart(severityCounts) {
    const ctx = document.getElementById('severityChart');
    if (!ctx) return;

    const labels = Object.keys(severityCounts);
    const values = Object.values(severityCounts);
    const colors = {
        'CRITICAL': '#d32f2f',
        'HIGH': '#f57c00',
        'MEDIUM': '#fbc02d',
        'LOW': '#388e3c',
        'INFO': '#1976d2'
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Findings by Severity',
                data: values,
                backgroundColor: labels.map(l => colors[l]),
                borderColor: labels.map(l => colors[l]),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Filter findings by severity
function filterBySeverity(severity) {
    const rows = document.querySelectorAll('.findings-table tbody tr');
    rows.forEach(row => {
        if (severity === 'all' || row.classList.contains(`severity-${severity.toLowerCase()}`)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
