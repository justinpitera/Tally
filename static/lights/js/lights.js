// static/js/lights.js

$(document).ready(function() {
    $('.toggle-light').click(function() {
        var lightId = $(this).data('light-id');
        // Implement the logic to toggle light
        // This could involve making an AJAX request to a Django view that controls the light
        console.log('Toggling light', lightId);
    });
});