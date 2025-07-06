const LOGISTIC_ANALYTICS_ENDPOINT = '/logistic_analytics_data';

function createTableCell(textContent) {
    const cell = document.createElement('td');
    cell.textContent = textContent;
    return cell;
}

async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        console.error('Failed to fetch data from ' + url + ': ' + response.status);
        throw new Error('Failed to fetch data: ' + response.status);
    }
    return await response.json();
}

const tableBody = document.getElementById('logistic-analytics-table-body');

function createConfidenceIntervalCell(ciLow, ciHigh) {
    // Display as [low, high] with 2 decimals
    const td = document.createElement('td');
    td.textContent = `[${ciLow.toFixed(2)}, ${ciHigh.toFixed(2)}]`;
    return td;
}

async function populateLogisticAnalyticsTable() {
    const analytics = await fetchData(LOGISTIC_ANALYTICS_ENDPOINT);
    tableBody.innerHTML = '';

    // Sort by effect size descending
    analytics.sort((a, b) => Math.abs(b.effect) - Math.abs(a.effect));

    analytics.forEach(item => {
        const row = tableBody.insertRow();
        row.appendChild(createTableCell(item.parameter));
        row.appendChild(createTableCell(item.effect.toFixed(3)));
        row.appendChild(createConfidenceIntervalCell(item.ci_low, item.ci_high));
        row.appendChild(createTableCell(item.p_value.toExponential(2)));
    });
}

populateLogisticAnalyticsTable();
