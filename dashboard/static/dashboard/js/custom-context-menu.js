document.addEventListener('DOMContentLoaded', function() {
    const notificationItems = document.querySelectorAll('.list-group-item');
    const customMenu = document.getElementById('customContextMenu');
    let timer;

    function showCustomMenu(e, notificationId) {
        e.preventDefault();

        const markReadLink = document.getElementById('markReadLink');
        markReadLink.href = getMarkAsReadUrl(notificationId);

        const feedBackLink = document.getElementById('feedBackLink'); // Ensure this ID matches the HTML
        const feedbackUrl = getFeedBackUrl(notificationId);
        feedBackLink.href = feedbackUrl;

        console.log(`Feedback URL set to: ${feedbackUrl}`); // Debugging: Log the feedback URL

        customMenu.style.left = `${e.pageX}px`;
        customMenu.style.top = `${e.pageY}px`;
        customMenu.style.display = 'block';
    }

    notificationItems.forEach(function(item) {
        item.addEventListener('contextmenu', function(e) {
            const notificationId = this.getAttribute('data-notification-id');
            showCustomMenu(e, notificationId);
        });

        item.addEventListener('touchstart', function(e) {
            e.preventDefault();
            timer = setTimeout(() => {
                showCustomMenu(e, this.getAttribute('data-notification-id'));
            }, 500);
        }, {passive: false});

        item.addEventListener('touchend', function() {
            clearTimeout(timer);
        });

        item.addEventListener('touchmove', function() {
            clearTimeout(timer);
        });
    });

    document.addEventListener('touchstart', hideCustomMenu);
    document.addEventListener('click', hideCustomMenu);

    function hideCustomMenu(e) {
        if (!customMenu.contains(e.target)) {
            customMenu.style.display = 'none';
        }
    }
});

function getFeedBackUrl(notificationId) {
    return `/notifications/view-feedback/${notificationId}/`; // Ensure this URL is correct
}
