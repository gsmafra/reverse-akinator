const ANALYTICS_ENDPOINT = '/monolithic_analytics_data';

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

function createConfidenceBar(p, ciLow, ciHigh, maxRight) {
    // All values are in [0, 1], maxRight is also in [0, 1]
    const container = document.createElement('div');
    container.className = 'ci-bar-container';

    // Scale all positions to [0, maxRight]
    const scale = x => (x / maxRight) * 100;

    // Bar for CI
    const bar = document.createElement('div');
    bar.className = 'ci-bar';
    bar.style.left = scale(ciLow) + '%';
    bar.style.width = (scale(ciHigh) - scale(ciLow)) + '%';

    // Marker for observed value
    const marker = document.createElement('div');
    marker.className = 'ci-marker';
    marker.style.left = scale(p) + '%';

    container.appendChild(bar);
    container.appendChild(marker);

    // Numbers label: only CI interval
    const label = document.createElement('div');
    label.style.fontSize = '0.9em';
    label.style.textAlign = 'center';
    label.style.marginTop = '2px';
    label.textContent = `[${(ciLow*100).toFixed(1)}%, ${(ciHigh*100).toFixed(1)}%]`;

    // Compose cell
    const td = document.createElement('td');
    td.appendChild(container);
    td.appendChild(label);
    return td;
}

async function populateAnalyticsTable() {
    const analytics = await fetchData(ANALYTICS_ENDPOINT);
    tableBody.innerHTML = '';

    // Find the max upper CI bound
    let maxUpper = 0;
    analytics.forEach(item => {
        if (item.ratio_thumbs_down_ci_high > maxUpper) {
            maxUpper = item.ratio_thumbs_down_ci_high;
        }
    });
    // Add a margin (e.g., 5%)
    let maxRight = Math.min(1, maxUpper + 0.05);

    // Sort ascending by thumbs down ratio
    analytics.sort((a, b) => a.ratio_thumbs_down - b.ratio_thumbs_down);

    analytics.forEach(item => {
        const row = tableBody.insertRow();
        row.appendChild(createTableCell(item.pipeline_name));
        row.appendChild(createTableCell(item.num_thumbs_down));
        row.appendChild(createTableCell(item.num_answers));
        const percent = (item.ratio_thumbs_down * 100).toFixed(1) + "%";
        row.appendChild(createTableCell(percent));
        // Graphical confidence interval bar, scaled
        row.appendChild(
            createConfidenceBar(
                item.ratio_thumbs_down,
                item.ratio_thumbs_down_ci_low,
                item.ratio_thumbs_down_ci_high,
                maxRight
            )
        );
    });
}

populateAnalyticsTable();
