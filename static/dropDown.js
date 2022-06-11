function myFunction() {
    document.getElementById("mydrop1").classList.toggle("show");
  }

window.onclick = function(event) {
    if (!event.target.matches('.dropdown-toggle')) {
      let dropdowns = document.getElementsByClassName("dropdown-item");
      let i;
      for (i = 0; i < dropdowns.length; i++) {
        let openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }