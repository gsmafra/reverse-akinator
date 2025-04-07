// Mock data
const items = [
    { character: 'Character 1', question: 'Question 1', answer: 'Answer 1' },
    { character: 'Character 2', question: 'Question 2', answer: 'Answer 2' },
    { character: 'Character 3', question: 'Question 3', answer: 'Answer 3' },
];

const answers = ['Answer 1', 'Answer 2', 'Answer 3', 'Answer 4', 'Answer 5'];

const tableBody = document.getElementById('table-body');

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
    defaultOption.textContent = "Select Rectified Answer";
    select.appendChild(defaultOption);
    answers.forEach(answer => {
        const option = document.createElement('option');
        option.value = answer;
        option.textContent = answer;
        select.appendChild(option);
    });
    rectifiedAnswerCell.appendChild(select);

    const submitCell = row.insertCell();
    const submitButton = document.createElement('button');
    submitButton.id = `submit-${index + 1}`;
    submitButton.textContent = 'Submit';
    submitButton.addEventListener('click', (e) => {
        const btnIndex = e.target.id.split('-')[1];
        const selectedAnswer = document.getElementById(`rectified-answer-${btnIndex}`).value;
        console.log(`Submitting rectified answer for item ${btnIndex}: ${selectedAnswer}`);
        // Make API call to submit rectified answer (in a real application)
    });
    submitCell.appendChild(submitButton);
});
