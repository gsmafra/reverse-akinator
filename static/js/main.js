document.addEventListener('DOMContentLoaded', function() {
    resetCharacter(); // Call the reset function when the page loads
});

function resetCharacter() {
    fetch('/reset', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            console.error('Error resetting character:', response.status);
            // Optionally display a message to the user
        }
        return response.json();
    })
    .then(data => {
        console.log('Reset successful:', data.message);
        // Optionally display a confirmation message to the user
    })
    .catch(error => {
        console.error('Error calling /reset:', error);
        // Optionally display an error message to the user
    });
}

function submitQuestion() {
    const questionInput = document.getElementById("question-input");
    const answerContainer = document.getElementById("answer-container");
    const question = questionInput.value.trim();

    if (question === "") {
        answerContainer.textContent = "Please enter a question.";
        return;
    }

    // Construct the URL with the question as a query parameter
    const url = `/yes_or_no?question=${encodeURIComponent(question)}`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json' // You might not need this for a simple GET
        },
        // No body is needed for a GET request
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Assuming your backend returns JSON
    })
    .then(data => {
        if (data && data.answer) {
            answerContainer.textContent = `Answer: ${data.answer}`;
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
        questionInput.value = ""; // Clear the input field
    });
}
