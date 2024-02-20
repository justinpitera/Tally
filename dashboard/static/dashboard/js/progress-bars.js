// progress-bars.js
// Created:     Tues Feb 20, 2024
// Last Edited: Tues Feb 20, 2024
// Author:      Justin Pitera
/*
    Purpose: To facilitate movement of the progress bars
*/



function updateAllCircularProgressBars() {
  document.querySelectorAll('.progress[data-grade]').forEach((progressElement, index) => {
    const gradePercentage = parseFloat(progressElement.getAttribute('data-grade'));
    insertKeyframeAnimations(index, gradePercentage);
    updateCircularProgressBar(progressElement, gradePercentage, index);
  });
}

function insertKeyframeAnimations(index, percentage) {
  const rightDegree = percentage > 50 ? 180 : (percentage / 50) * 180;
  const leftDegree = percentage > 50 ? ((percentage - 50) / 50) * 180 : 0;

  const styleSheet = document.createElement("style");
  styleSheet.type = "text/css";
  styleSheet.innerText = `
    @keyframes rotateRight${index} {
        from { transform: rotate(0deg); }
        to { transform: rotate(${rightDegree}deg); }
    }
    @keyframes rotateLeft${index} {
        from { transform: rotate(0deg); }
        to { transform: rotate(${leftDegree}deg); }
    }
  `;
  document.head.appendChild(styleSheet);
}

function updateCircularProgressBar(progressElement, percentage, index) {
  const leftBar = progressElement.querySelector('.progress-left .progress-bar');
  const rightBar = progressElement.querySelector('.progress-right .progress-bar');
  const progressValue = progressElement.querySelector('.progress-value');

  // Initiate the bar animations
  rightBar.style.animation = `rotateRight${index} 1s linear forwards`;
  if (percentage > 50) {
    leftBar.style.animation = `rotateLeft${index} 1s linear forwards 1s`; // Starts after the right bar animation
  }

  // Duration of animation in milliseconds
  const animationDuration = percentage > 50 ? 2000 : 1000; // Adjust based on your actual animation times
  
  let startPercentage = 0;
  const stepTime = animationDuration / percentage;

  function updateText() {
    startPercentage++;
    progressValue.textContent = `${startPercentage}%`;

    // Stop the interval when the target percentage is reached
    if (startPercentage >= percentage) {
      clearInterval(interval);
    }
  }

  // Update the progress text at each step
  const interval = setInterval(updateText, stepTime);
}


// Initialize the progress bars on document ready
document.addEventListener('DOMContentLoaded', (event) => {
  updateAllCircularProgressBars();
});












