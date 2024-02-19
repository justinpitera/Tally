


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
  
    rightBar.style.animation = `rotateRight${index} 1s linear forwards`;
    if (percentage > 50) {
      leftBar.style.animation = `rotateLeft${index} 1s linear forwards 1s`; // Ensure this starts after the right bar animation
    }
  
    progressValue.textContent = `${percentage}%`;
  }
  
  // Initialize the progress bars on document ready
  document.addEventListener('DOMContentLoaded', (event) => {
    updateAllCircularProgressBars();
  });
  
  
  
  
      function showAvailable() {
          document.getElementById("availableAssignments").style.display = "block";
          document.getElementById("upcomingAssignments").style.display = "none";
          document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active-tab'));
          event.target.classList.add('active-tab');
      }
      function showUpcoming() {
          document.getElementById("upcomingAssignments").style.display = "block";
          document.getElementById("availableAssignments").style.display = "none";
          document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active-tab'));
          event.target.classList.add('active-tab');
      }
  
        document.addEventListener('DOMContentLoaded', (event) => {
          // Check if the card was previously closed
          if (localStorage.getItem('cardClosed') === 'true') {
            document.querySelector('.card').style.display = 'none';
          }
        
          document.querySelector('.close').addEventListener('click', function(e) {
            e.preventDefault();
            this.closest('.card').style.display = 'none';
            // Save the closed state in localStorage
            localStorage.setItem('cardClosed', 'true');
          });
        });