// scroll-to-bottom.js
// Created:     Tues Feb 20, 2024
// Last Edited: Tues Feb 20, 2024
// Author:      Justin Pitera
/*
    Purpose: If the user clicks on the scroll indicator, it will bring them to the bottom of the page.
*/
function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}