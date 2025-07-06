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
const baselineTdRateSpan = document.getElementById('baseline-td-rate');

function createConfidenceIntervalCell(ciLow, ciHigh) {
    // Display as [low, high] with 2 decimals
    const td = document.createElement('td');
    td.textContent = `[${ciLow.toFixed(2)}, ${ciHigh.toFixed(2)}]`;
    return td;
}

function logitToProb(logit) {
    return 1 / (1 + Math.exp(-logit));
}

async function populateLogisticAnalyticsTable() {
    const result = await fetchData(LOGISTIC_ANALYTICS_ENDPOINT);
    // result should have: baseline_td_rate, effects (array)
    const effects = result.effects;
    const baselineTdRate = result.baseline_td_rate;
    tableBody.innerHTML = '';
    if (baselineTdRateSpan) {
        baselineTdRateSpan.textContent = (baselineTdRate * 100).toFixed(1) + '%';
    }

    // Sort by effect size descending
    effects.sort((a, b) => Math.abs(b.effect) - Math.abs(a.effect));

    effects.forEach(item => {
        const row = tableBody.insertRow();
        row.appendChild(createTableCell(item.parameter));
        row.appendChild(createTableCell(item.effect.toFixed(3)));
        row.appendChild(createConfidenceIntervalCell(item.ci_low, item.ci_high));
        row.appendChild(createTableCell((item.delta_td_rate * 100).toFixed(1) + '%'));
        // Show CI for delta_td_rate
        if (item.delta_td_rate_ci_low !== undefined && item.delta_td_rate_ci_high !== undefined) {
            row.appendChild(createConfidenceIntervalCell(item.delta_td_rate_ci_low * 100, item.delta_td_rate_ci_high * 100));
        } else {
            row.appendChild(createTableCell(''));
        }
        row.appendChild(createTableCell(item.p_value.toExponential(2)));
    });
}

populateLogisticAnalyticsTable();
