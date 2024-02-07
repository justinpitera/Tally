
  function toggleCommentForm(button) {
    const commentForm = button.nextElementSibling; // Assumes the comment form is right after the button
    const isVisible = commentForm.style.display === 'block';
    // Toggle comment form visibility
    commentForm.style.display = isVisible ? 'none' : 'block';
    
    // Prevent the list-group-item link from being followed
    event.preventDefault();
  }
  
  // Optional: Hide comment form when clicking outside
  window.addEventListener('click', function(event) {
    document.querySelectorAll('.comment-form').forEach(function(commentForm) {
      if (!commentForm.contains(event.target) && !event.target.matches('button')) {
        commentForm.style.display = 'none';
      }
    });
  });

    document.addEventListener('DOMContentLoaded', function() {
        // Select all download buttons by class
        var downloadButtons = document.querySelectorAll('.custom-download-btn');
    
        // Add click event listener to each button
        downloadButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                // Prevent the default action
                event.preventDefault();
    
                // Get the URL from the data-url attribute of the button
                var url = this.getAttribute('data-url');
                
                // Open the URL in a new tab
                window.open(url, '_blank');
            });
        });
    });

    function showSection(sectionId) {
      // Hide all sections
      document.querySelectorAll('.content-section').forEach(function(section) {
        section.style.display = 'none';
      });
    
      // Show the selected section
      document.getElementById(sectionId).style.display = 'block';
    
      // Update nav link active state
      document.querySelectorAll('.nav-link').forEach(function(link) {
        link.classList.remove('active');
      });
      event.currentTarget.classList.add('active');
    }

    
  document.addEventListener('DOMContentLoaded', function() {
      // Function to show a specific section
      function showSection(sectionId) {
          // Hide all sections
          document.querySelectorAll('.content-section').forEach(function(section) {
              section.style.display = 'none';
          });
  
          // Show the selected section
          const sectionToShow = document.getElementById(sectionId);
          if (sectionToShow) {
              sectionToShow.style.display = 'block';
          } else {
              console.error("Section with ID '" + sectionId + "' not found.");
          }
  
          // Update nav link active state
          document.querySelectorAll('.nav-link').forEach(function(link) {
              link.classList.remove('active');
              if(link.getAttribute('onclick').includes(sectionId)) {
                  link.classList.add('active');
              }
          });
      }
  
      // Immediately invoked function to handle auto-tab functionality based on URL query
      (function handleAutoTab() {
          const urlParams = new URLSearchParams(window.location.search);
          const tab = urlParams.get('tab'); // Get 'tab' parameter from URL
          
          if (tab) {
              showSection(tab); // Call showSection with the ID corresponding to the tab parameter
          }
      })();
  
      // Add event listeners for other functionalities as previously defined
      // Handling file input changes, toggling comment forms, etc.
      // ...
  
      document.querySelector('.custom-file-input')?.addEventListener('change', function(e) {
          var fileName = e.target.files[0].name;
          var nextSibling = e.target.nextElementSibling;
          nextSibling.innerText = fileName;
      });
  });
  
  // Define other functions (toggleCommentForm, etc.) here as needed.
  var downloadButtons = document.querySelectorAll('.custom-download-btn');

  // Add click event listener to each button
  downloadButtons.forEach(function(button) {
      button.addEventListener('click', function(event) {
          // Prevent the default action
          event.preventDefault();

          // Get the URL from the data-url attribute of the button
          var url = this.getAttribute('data-url');
          
          // Open the URL in a new tab
          window.open(url, '_blank');
      });
  });
  

    document.addEventListener('DOMContentLoaded', function() {
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(function(section) {
                section.style.display = 'none';
            });
    
            // Show the selected section
            var sectionToShow = document.getElementById(sectionId);
            if (sectionToShow) {
                sectionToShow.style.display = 'block';
            }
    
            // Update nav link active state
            document.querySelectorAll('.nav-pills .nav-link').forEach(function(link) {
                if(link.getAttribute('onclick').includes(sectionId)) {
                    document.querySelectorAll('.nav-pills .nav-link').forEach(function(l) { l.classList.remove('active'); });
                    link.classList.add('active');
                }
            });
        }
    
        // Read the 'tab' query parameter from the URL
        const urlParams = new URLSearchParams(window.location.search);
        const tab = urlParams.get('tab');
    
        // If 'tab' parameter exists and it's 'section2', show Section 2 by default
        if (tab) {
            showSection(tab);
        }
    
        // Listen for changes in the file input
        document.querySelector('.custom-file-input')?.addEventListener('change', function(e) {
            var fileName = e.target.files[0].name;
            var nextSibling = e.target.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    });
    
    // You may keep other JavaScript functions and event listeners here as needed.
