


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


      document.addEventListener('DOMContentLoaded', function() {
        const notificationItems = document.querySelectorAll('.list-group-item');
        const customMenu = document.getElementById('customContextMenu');
        let timer;
    
        function showCustomMenu(e, notificationId) {
            // Prevent the default context menu
            e.preventDefault();
    
            // Update the href for the mark as read link
            const markReadLink = document.getElementById('markReadLink');
            markReadLink.href = getMarkAsReadUrl(notificationId);
    
            // Set custom menu position
            customMenu.style.left = `${e.pageX}px`;
            customMenu.style.top = `${e.pageY}px`;
            customMenu.style.display = 'block';
        }
    
        notificationItems.forEach(function(item) {
            item.addEventListener('contextmenu', function(e) {
                const notificationId = this.getAttribute('data-notification-id');
                showCustomMenu(e, notificationId);
            });
    
            // Listen for touchstart event for long-press
            item.addEventListener('touchstart', function(e) {
                // Prevent the default long press behavior of iOS
                e.preventDefault();
    
                // Start a timer to detect long press
                timer = setTimeout(() => {
                    showCustomMenu(e, this.getAttribute('data-notification-id'));
                }, 500); // 500ms for long press
            }, {passive: false});
    
            // Cancel the timer if the touch ends before the long press duration
            item.addEventListener('touchend', function(e) {
                clearTimeout(timer);
            });
    
            item.addEventListener('touchmove', function(e) {
                clearTimeout(timer);
            });
        });
    
        // Hide the custom menu on touch or click elsewhere
        document.addEventListener('touchstart', hideCustomMenu);
        document.addEventListener('click', hideCustomMenu);
    
        function hideCustomMenu(e) {
            if (!customMenu.contains(e.target)) {
                customMenu.style.display = 'none';
            }
        }
    });
    
    function getMarkAsReadUrl(notificationId) {
        // Adjust this function to match your URL scheme
        return "/notifications/mark-as-read/" + notificationId + "/";
    }










