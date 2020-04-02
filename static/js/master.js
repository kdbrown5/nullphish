function checknav() {
  var w = window.innerWidth;
  var h = window.innerHeight;
  if (w < 1080) {
    document.getElementById("menu").style.display = "none"; 
    document.getElementById("dropdown").style.display = "inline-block"; 
  }
  else {
    document.getElementById("menu").style.display = "table"; 
    document.getElementById("dropdown").style.display = "none"; 
  }
}