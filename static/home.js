// document.getElementById("myBtn").addEventListener("click", closenav);
// function closenav() {
//   alert("hello");
// }

var navhamburger = document.getElementsByClassName("navhamburger");
navhamburger[0].addEventListener("click", ()=> {
  document.querySelector(".navdivs.nav2").classList.toggle("nav2-show-hide");

  let cross = document.querySelector(".cross");
  cross.addEventListener("click", ()=> {
    document.querySelector(".navdivs.nav2").classList.remove("nav2-show-hide");
  })
});