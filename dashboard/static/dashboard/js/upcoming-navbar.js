// upcoming-navbar.js
// Created:     Tues Feb 20, 2024
// Last Edited: Tues Feb 20, 2024
// Author:      Justin Pitera
/*
    Purpose: To operate the navigation of the upcoming tab. 
*/


document.querySelectorAll('.nav-link').forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent default anchor behavior
      
      const targetId = this.getAttribute('data-target'); // Get the target content ID
      document.querySelectorAll('.content-div').forEach(div => {
        div.style.display = 'none'; // Hide all content divs
      });
      const targetDiv = document.getElementById(targetId);
      targetDiv.style.display = 'block'; // Show the target content div
  
      // Update active class for pills
      document.querySelectorAll('.nav-link').forEach(nav => {
        nav.classList.remove('active');
      });
      this.classList.add('active'); // Set current pill as active
  
      scrollToView(targetDiv); // Scroll to make the div fully visible if needed
    });
  });
  
  function scrollToView(element) {
    const rect = element.getBoundingClientRect(); // Get the position of the element relative to the viewport
      window.scrollBy({ top: rect.bottom - window.innerHeight + 100, behavior: 'smooth' }); // Scroll down to make element fully visible. Adjust the 20px offset as needed.
  }