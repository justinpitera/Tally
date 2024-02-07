document.addEventListener('DOMContentLoaded', function () {
    // Attach click event listeners to all tab links
    var tabLinks = document.querySelectorAll('.nav-link');
    tabLinks.forEach(function(tabLink) {
        tabLink.addEventListener('click', function(event) {
            event.preventDefault();

            // Deactivate all tabs and contents
            deactivateAllTabsAndContents(tabLinks);

            // Activate clicked tab and its content
            activateTabAndContent(this);
        });
    });

    // Function to deactivate all tabs and contents
    function deactivateAllTabsAndContents(tabLinks) {
        tabLinks.forEach(function(link) {
            link.classList.remove('active');
            var contentId = link.getAttribute('href');
            var tabContent = document.querySelector(contentId);
            if (tabContent) {
                tabContent.classList.remove('show', 'active');
            }
        });
    }

    // Function to activate tab and its content
    function activateTabAndContent(tabLink) {
        tabLink.classList.add('active');
        var contentId = tabLink.getAttribute('href');
        var tabContent = document.querySelector(contentId);
        if (tabContent) {
            tabContent.classList.add('show', 'active');
        }
    }

    // Check if URL contains query parameter for a specific tab
    var urlParams = new URLSearchParams(window.location.search);
    var tabParam = urlParams.get('tab');
    if (tabParam) {
        var tabToActivate = document.querySelector(`#${tabParam}-tab`);
        if (tabToActivate) {
            activateTabAndContent(tabToActivate);
        }
    } else {
        // Optionally, activate the first tab by default if no tab parameter is found
        if (tabLinks.length > 0) {
            activateTabAndContent(tabLinks[0]);
        }
    }
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
});
