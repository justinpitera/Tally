// scroll-indicator.js
// Created:     Tues Feb 20, 2024
// Last Edited: Tues Feb 20, 2024
// Author:      Justin Pitera
/*
    Purpose: To show a scroll indicator if the user cannot see the entire pages contents.
*/

function checkScrollIndicatorVisibility() {
    var windowSize = window.innerHeight;
    var bodyHeight = document.body.offsetHeight;
    var bottomOffset = 100; 

    // Initially check if the content is taller than the viewport
    if (bodyHeight <= windowSize) {
        // Hide the indicator if the content doesn't overflow the viewport
        document.querySelector('.scroll-indicator').style.display = 'none';
    } else {
        // Show the indicator by default if content overflows
        document.querySelector('.scroll-indicator').style.display = 'block';
        
        // Calculate the bottom position for the current scroll
        var scrollPosition = window.scrollY;
        var bottomPosition = bodyHeight - windowSize - bottomOffset;

        if (scrollPosition >= bottomPosition) {
            // Hide the indicator if scrolled near the bottom
            document.querySelector('.scroll-indicator').style.display = 'none';
        } else {
            // Show the indicator if not near the bottom
            document.querySelector('.scroll-indicator').style.display = 'block';
        }
    }
}

// Check and adjust scroll indicator on document load
document.addEventListener('DOMContentLoaded', checkScrollIndicatorVisibility);

// Adjust scroll indicator visibility on window resize
window.addEventListener('resize', checkScrollIndicatorVisibility);

// Adjust scroll indicator visibility on scroll
document.addEventListener('scroll', checkScrollIndicatorVisibility);
