let sessionHistory = [];

function updateSessionHistoryList(sessionAnswers) {
    const sessionHistoryList = document.getElementById("session-history-list");
    sessionHistoryList.innerHTML = "";
  
    sessionAnswers.forEach((answer, index) => {
      const listItem = document.createElement("li");
      const questionSpan = document.createElement("span");
      const answerSpan = document.createElement("span");
  
      questionSpan.className = "question";
      answerSpan.className = "answer";
  
      questionSpan.textContent = answer.question;
      answerSpan.textContent = answer.answer;
  
      listItem.appendChild(questionSpan);
      listItem.appendChild(document.createElement("br"));
      listItem.appendChild(answerSpan);
  
      sessionHistoryList.appendChild(listItem);
    });
  }
