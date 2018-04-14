var navbar = document.getElementById("topnavbar");

function myFunction() {
    if (navbar.className === "topnav") {
        navbar.className += " responsive";
    } else {
        navbar.className = "topnav";
    }
};

var height = navbar.offsetHeight;
var dropcontent = document.getElementsByClassName('dropdown-content');

for(i = 0; i < dropcontent.length; i++) {
  dropcontent[i].style.marginTop = height + "px";
};
