document.addEventListener('DOMContentLoaded', (event) => {
    // Get the popup element
  var popup = document.getElementById("popupMenu");
  
  // Get the button that opens the popup
  var btn = document.getElementById("openPopupBtn");
  
  // Get the <span> element that closes the popup
  var span = document.getElementById("closePopupBtn");
  
  // When the user clicks the button, open the popup 
  btn.onclick = function() {
    popup.style.display = "block";
  }
  
  // When the user clicks on <span> (x), close the popup
  span.onclick = function() {
    popup.style.display = "none";
  }
  
  // When the user clicks anywhere outside of the popup, close it
  window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = "none";
    }
  }
  });
  document.addEventListener('DOMContentLoaded', function() {
    var toggleButton = document.getElementById('darkModeToggle');

    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
    });
});
