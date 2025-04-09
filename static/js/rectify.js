const tableBody = document.getElementById('table-body');
const answers = ['yes', 'no', 'ambiguous']; // These are the options for rectification

async function populateTable() {
    try {
        const response = await fetch('/answers_to_rectify');
        if (!response.ok) {
            console.error(`Failed to fetch data: ${response.status}`);
            // Optionally display an error message to the user
            return;
        }
        const items = await response.json();

        // Clear any existing rows in the table
        tableBody.innerHTML = '';

        items.forEach((item, index) => {
            const row = tableBody.insertRow();

            const characterCell = row.insertCell();
            characterCell.textContent = item.character;

            const questionCell = row.insertCell();
            questionCell.textContent = item.question;

            const answerCell = row.insertCell();
            answerCell.textContent = item.answer;

            const rectifiedAnswerCell = row.insertCell();
            const select = document.createElement('select');
            select.id = `rectified-answer-${index + 1}`;
            const defaultOption = document.createElement('option');
            defaultOption.value = "";
            defaultOption.textContent = "Select Answer";
            select.appendChild(defaultOption);
            answers.forEach(answer => {
                const option = document.createElement('option');
                option.value = answer;
                option.textContent = answer;
                select.appendChild(option);
            });
            rectifiedAnswerCell.appendChild(select);

            // --- Submit Button Mocked Out ---
            const submitCell = row.insertCell();
            const submitButton = document.createElement('button');
            submitButton.id = `submit-${index + 1}`;
            submitButton.textContent = 'Submit';
            // We are intentionally NOT adding an event listener to the submit button
            submitCell.appendChild(submitButton);
            // --- End of Mocked Out Submit Button ---
        });

    } catch (error) {
        console.error("Error fetching data:", error);
        // Optionally display an error message to the user
    }
}

// Call populateTable when the page loads to fetch and display the initial data
populateTable();
