function checkcontainers() {
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