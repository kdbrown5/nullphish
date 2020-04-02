function checknav() {
  var w = window.outerWidth;
  var h = window.outerHeight;
  if (w < 1200) {
    document.getElementById("mainmenu").style.display = "none"; 
    document.getElementById("dropdown").style.display = "inline-block"; 
  }
  else {
    document.getElementById("mainmenu").style.display = "initial"; 
    document.getElementById("dropdown").style.display = "none"; 
  }
}

function checkcontentontainers() {
  var w = window.outerWidth;
  var h = window.outerHeight;
  if (w < 1080) {
    document.getElementById("tilecontainer").style.display = "none"; 
    document.getElementById("tilelist").style.display = "block"; 
  }
  else {
    document.getElementById("tilecontainer").style.display = "grid"; 
    document.getElementById("tilelist").style.display = "none"; 
  }
}

function toggledropdown() {
  if (document.getElementById("dropcontent").style.display = "none") {
    document.getElementById("dropcontent").style.display = "block";
  }
  else {
    document.getElementById("dropcontent").style.display = "none";
  }
}