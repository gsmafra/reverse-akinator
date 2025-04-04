const askButton = document.getElementById("ask-button");
const questionInput = document.getElementById("question-input");
const answerContainer = document.getElementById("answer-container");

function submitQuestion() {
    const question = questionInput.value.trim();

    if (question === "") {
        answerContainer.textContent = "Please enter a question.";
        return;
    }

    // Disable the button and show the loading spinner
    askButton.disabled = true;
    askButton.innerHTML = 'Asking... <span class="loading-spinner"></span>';

    // Construct the URL with the question as a query parameter
    const url = `/ask?question=${encodeURIComponent(question)}`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data && data.answer !== null && data.answer !== undefined) {
            const answerText = data.answer ? 'Yes' : 'No';
            answerContainer.textContent = `Answer: ${answerText}`;
            updateSessionHistoryList(data.session_answers);
            answerContainer.classList.remove('error'); // Remove error class if present
        } else {
            answerContainer.textContent = "Error: Invalid response from server.";
            answerContainer.classList.add('error'); // Add error class for styling
        }
    })
    .catch(error => {
        console.error('Error calling backend:', error);
        answerContainer.textContent = "Error communicating with the server.";
        answerContainer.classList.add('error'); // Add error class for styling
    })
    .finally(() => {
        // Re-enable the button and reset its text
        askButton.disabled = false;
        askButton.innerHTML = 'Ask!';
        questionInput.value = ""; // Clear the input field
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const askButton = document.getElementById("ask-button"); // Re-declare if needed inside the listener
    askButton.addEventListener('click', submitQuestion);
});
