// custom-context-menu.js
// Created:     Tues Feb 20, 2024
// Last Edited: Tues Feb 20, 2024
// Author:      Justin Pitera
/*
    Purpose: To operate the custom context menu of the each notification
*/

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
