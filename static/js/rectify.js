const RECTIFY_ENDPOINT = '/rectify_answer';
const ANSWERS_TO_RECTIFY_ENDPOINT = '/answers_to_rectify';
const RECTIFICATION_OPTIONS = ['yes', 'no', 'ambiguous'];

function createTableCell(textContent) {
    const cell = document.createElement('td');
    cell.textContent = textContent;
    return cell;
}

function createSelectElement(id, options) {
    const select = document.createElement('select');
    select.id = id;
    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "Select Answer";
    select.appendChild(defaultOption);
    options.forEach(optionValue => {
        const option = document.createElement('option');
        option.value = optionValue;
        option.textContent = optionValue;
        select.appendChild(option);
    });
    return select;
}

function createButtonElement(id, text, onClickHandler) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    button.addEventListener('click', onClickHandler);
    return button;
}

async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        console.error('Failed to fetch data from ' + url + ': ' + response.status);
        throw new Error('Failed to fetch data: ' + response.status);
    }
    return await response.json();
}

async function submitRectification(data) {
    const response = await fetch(RECTIFY_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        console.error('Failed to submit rectification: ' + response.status);
        throw new Error('Failed to submit rectification.');
    }
    return response; // Or response.json() if your backend returns data
}

const tableBody = document.getElementById('table-body');

async function populateTable() {
    const items = await fetchData(ANSWERS_TO_RECTIFY_ENDPOINT);
    tableBody.innerHTML = '';

    items.forEach((item, index) => {
        const row = tableBody.insertRow();

        row.appendChild(createTableCell(item.character));
        row.appendChild(createTableCell(item.question));
        row.appendChild(createTableCell(item.answer));

        const rectifiedAnswerCell = row.insertCell();
        const selectId = 'rectified-answer-' + (index + 1);
        const select = createSelectElement(selectId, RECTIFICATION_OPTIONS);
        rectifiedAnswerCell.appendChild(select);

        const submitCell = row.insertCell();
        const submitId = 'submit-' + (index + 1);
        const submitButton = createButtonElement(submitId, 'Submit', async () => {
            const selectedRectifiedAnswer = document.getElementById(selectId).value;
            if (!selectedRectifiedAnswer) {
                alert('Please select a rectified answer.');
                return;
            }

            const data = {
                character: item.character,
                question: item.question,
                rectified_answer: selectedRectifiedAnswer
            };

            try {
                const response = await submitRectification(data);
                if (response.ok) {
                    // Remove the submit button on successful submission
                    submitCell.removeChild(submitButton);
                } else {
                    alert('Failed to submit rectification.');
                }
            } catch (error) {
                alert('Error submitting rectification.');
            }
        });
        submitCell.appendChild(submitButton);
    });
}

populateTable();
