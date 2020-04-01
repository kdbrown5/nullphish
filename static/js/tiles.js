function checkcontainers() {
  var w = window.innerWidth;
  var h = window.innerHeight;
  if (w < 500) {
    document.getElementById("tilecontainer").style.display = "none"; 
    document.getElementById("tilelist").style.display = "block"; 
  }
  else {
    document.getElementById("tilecontainer").style.display = "grid"; 
    document.getElementById("tilelist").style.display = "none"; 
  }
}