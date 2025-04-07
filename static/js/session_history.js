function updateSessionHistoryList(sessionAnswers) {
  const sessionHistoryList = document.getElementById("session-history-list");
  sessionHistoryList.innerHTML = "";

  sessionAnswers.forEach((answer, index) => {
      const listItem = document.createElement("li");
      const questionSpan = document.createElement("span");
      const answerSpan = document.createElement("span");
      const thumbsDownButton = document.createElement("button");
      thumbsDownButton.className = "thumbs-down-button";
      thumbsDownButton.textContent = "👎";

      questionSpan.className = "question";
      answerSpan.className = "answer";

      questionSpan.textContent = answer.question;
      answerSpan.textContent = answer.answer;

      listItem.appendChild(questionSpan);
      listItem.appendChild(document.createElement("br"));
      listItem.appendChild(answerSpan);
      listItem.appendChild(thumbsDownButton);

      sessionHistoryList.appendChild(listItem);

      handleThumbsDownButtonClick(thumbsDownButton, answer);
  });
}

function handleThumbsDownButtonClick(thumbsDownButton, answer) {
  thumbsDownButton.addEventListener("click", () => {
      const question = answer.question;
      const characterText = document.getElementById('revealed-character').textContent;
      const character = characterText.replace('The character is: ', '');
      const answerText = answer.answer;

      fetch('/thumbs_down', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              question: question,
              character: character,
              answer: answerText
          })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));

      thumbsDownButton.classList.add("clicked");
      thumbsDownButton.style.pointerEvents = "none";
      thumbsDownButton.disabled = true;
  });
}
