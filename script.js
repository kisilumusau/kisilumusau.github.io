function toggleDetails() {
    const details = document.getElementById("spotlightDetails1");
    details.style.display = (details.style.display === "none" || details.style.display === "") 
      ? "block" 
      : "none";
  }
  
  function toggleDetails2() {
    const details = document.getElementById("spotlightDetails2");
    details.style.display = (details.style.display === "none" || details.style.display === "") 
      ? "block" 
      : "none";
  }
  
  function toggleDetails3() {
    const details = document.getElementById("spotlightDetails3");
    details.style.display = (details.style.display === "none" || details.style.display === "") 
      ? "block" 
      : "none";
  }
  function checkAnswer() {
    const answer = document.getElementById('riddle-answer').value.trim().toLowerCase();
    const feedback = document.getElementById('riddle-feedback');
    const secretSection = document.getElementById('secret-section');
    
    if (answer === "echo") {
      feedback.textContent = "Correct! 🎉 Unveiling the secret...";
      feedback.style.color = "green";
      secretSection.style.display = "block";
    } else {
      feedback.textContent = "Oops! Try again. Hint: It's something that comes back when you call.";
      feedback.style.color = "red";
    }
  }
  
  