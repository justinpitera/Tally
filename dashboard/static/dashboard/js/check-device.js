if (('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) {
    document.getElementById('changeMe').innerHTML = 'To view your feedback, hold ';
} else {
    document.getElementById('changeMe').innerHTML = 'To view your feedback, click';
}
