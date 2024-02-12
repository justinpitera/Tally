document.addEventListener('DOMContentLoaded', function () {
    var tabLinks = document.querySelectorAll('.nav-link:not(.dropdown-toggle)');
    var dropdownLinks = document.querySelectorAll('.dropdown-menu a');

    // Function to deactivate all tabs and contents
    function deactivateAllTabsAndContents() {
        tabLinks.forEach(function(link) {
            if (!link.classList.contains('dropdown-toggle')) { // Check to ensure it's not a dropdown toggle link
                link.classList.remove('active');
                var contentId = link.getAttribute('href');
                var tabContent = document.querySelector(contentId);
                if (tabContent) {
                    tabContent.classList.remove('show', 'active');
                }
            }
        });
    }

    // Function to activate tab and its content
    function activateTabAndContent(tabLink) {
        if (!tabLink.classList.contains('dropdown-toggle')) { // Again, ensure it's not a dropdown toggle
            tabLink.classList.add('active');
            var contentId = tabLink.getAttribute('href');
            var tabContent = document.querySelector(contentId);
            if (tabContent) {
                tabContent.classList.add('show', 'active');
            }
        }
    }

    // Attach click event listeners to all tab links, excluding the dropdown toggle
    tabLinks.forEach(function(tabLink) {
        tabLink.addEventListener('click', function(event) {
            event.preventDefault();

            // Deactivate all tabs and contents, ensuring dropdown interactions are excluded
            deactivateAllTabsAndContents();

            // Activate clicked tab and its content, ensuring dropdown interactions are excluded
            activateTabAndContent(this);
        });
    });

    // No changes required here for dropdownLinks, as we're not modifying dropdown behavior directly
    dropdownLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.stopPropagation(); // This remains to prevent unintended behavior, but the primary issue is addressed above
        });
    });

    // The remaining part of the script for activating tabs based on URL parameters or default logic remains unchanged
});

 document.addEventListener('DOMContentLoaded', function () {
    // Check if the URL contains the query parameter for the Assignments tab
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('tab') === 'assignments') {
       // Deactivate currently active tab and its content
       document.querySelector('.nav-link.active').classList.remove('active');
       document.querySelector('.tab-pane.fade.show.active').classList.remove('show', 'active');
       
       // Activate the Assignments tab
       document.getElementById('profile-tab').classList.add('active');
       // Activate the Assignments tab content
       var assignmentsContent = document.getElementById('profile');
       assignmentsContent.classList.add('show', 'active');
   }
   if (urlParams.get('tab') === 'onlinelearning') {
    // Deactivate currently active tab and its content
    document.querySelector('.nav-link.active').classList.remove('active');
    document.querySelector('.tab-pane.fade.show.active').classList.remove('show', 'active');
    
    // Activate the Assignments tab
    document.getElementById('online-learning-tab').classList.add('active');
    // Activate the Assignments tab content
    var assignmentsContent = document.getElementById('online-learning');
    assignmentsContent.classList.add('show', 'active');
}
});

document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const resultsTableBody = document.getElementById('resultsTableBody'); // Make sure this is your table body ID
    const courseId = searchForm.getAttribute('data-course-id'); // Ensure this is correctly obtaining the course ID

    function fetchAndDisplayUsers(query) {
        fetch(`/ajax/search-users/${courseId}/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsTableBody.innerHTML = ''; // Clear existing rows
                data.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${user.username}</td><td>${user.email}</td><td>${user.average_grade}</td>`; // Now includes average grade
                    resultsTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    // Load all students on initial page load
    fetchAndDisplayUsers('');

    // Re-fetch students based on search query
    searchForm.addEventListener("submit", function(e) {
        e.preventDefault();
        fetchAndDisplayUsers(searchInput.value);
    });
});

    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('search-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const searchQuery = document.getElementById('search-query').value;
            fetch(`your_view_url?search_query=${encodeURIComponent(searchQuery)}`)
            .then(response => response.text())
            .then(html => {
                document.getElementById('assignments-container').innerHTML = html;
            });
        });
    });