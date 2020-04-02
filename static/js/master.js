function checknav() {
  var w = window.innerWidth;
  var h = window.innerHeight;
  if (w < 1080) {
    document.getElementById("mainmenu").style.display = "none"; 
    document.getElementById("dropdown").style.display = "inline-block"; 
  }
  else {
    document.getElementById("mainmenu").style.display = "initial"; 
    document.getElementById("dropdown").style.display = "none"; 
  }
}