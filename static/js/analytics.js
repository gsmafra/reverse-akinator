const ANALYTICS_ENDPOINT = '/analytics_data';

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

const tableBody = document.getElementById('analytics-table-body');

async function populateAnalyticsTable() {
    const analytics = await fetchData(ANALYTICS_ENDPOINT);
    tableBody.innerHTML = '';

    analytics.forEach(item => {
        const row = tableBody.insertRow();
        row.appendChild(createTableCell(item.pipeline_name));
        row.appendChild(createTableCell(item.num_thumbs_down));
        row.appendChild(createTableCell(item.num_answers));
        // Format percentage
        const percent = (item.ratio_thumbs_down * 100).toFixed(1) + "%";
        row.appendChild(createTableCell(percent));
        // Format confidence interval
        const ciLow = (item.ratio_thumbs_down_ci_low * 100).toFixed(1);
        const ciHigh = (item.ratio_thumbs_down_ci_high * 100).toFixed(1);
        const ciString = `[${ciLow}%, ${ciHigh}%]`;
        row.appendChild(createTableCell(ciString));
    });
}

populateAnalyticsTable();
