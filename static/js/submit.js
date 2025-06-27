import { getDeviceId } from './device_id.js';
import { updateSessionHistoryList } from './session_history.js';

const askButton = document.getElementById("ask-button");
const questionInput = document.getElementById("question-input");
const answerContainer = document.getElementById("answer-container");

function submitQuestion() {
    const question = questionInput.value.trim();

    if (question === "") {
        answerContainer.textContent = "Please enter a question.";
        return;
    }

    askButton.disabled = true;
    askButton.innerHTML = '<span class="loading-spinner"></span>';

    const url = `/ask?question=${encodeURIComponent(question)}&device_id=${getDeviceId()}`;

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
            const answerText = data.answer === 'yes' ? 'Yes' : data.answer === 'no' ? 'No' : 'Ambiguous';
            answerContainer.textContent = `Answer: ${answerText}`;
            updateSessionHistoryList(data.session_answers);
            answerContainer.classList.remove('error');
        } else {
            answerContainer.textContent = "Error: Invalid response from server.";
            answerContainer.classList.add('error');
        }
    })
    .catch(error => {
        console.error('Error calling backend:', error);
        answerContainer.textContent = "Error communicating with the server.";
        answerContainer.classList.add('error');
    })
    .finally(() => {
        askButton.disabled = false;
        askButton.innerHTML = 'Ask!';
        questionInput.value = "";
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const askButton = document.getElementById("ask-button");
    askButton.addEventListener('click', submitQuestion);
});

questionInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        askButton.click();
    }
});
