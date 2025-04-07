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
      thumbsDownButton.classList.add("clicked");
      thumbsDownButton.style.pointerEvents = "none";
      thumbsDownButton.disabled = true;
      // Mock a call to a POST thumbs down
      console.log(`Thumbs down clicked for question: ${answer.question}`);
      // TODO: Implement actual POST request
  });
}
