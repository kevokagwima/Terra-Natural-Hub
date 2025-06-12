const hamburger = document.querySelector(".hamburger-side");
const menu = document.querySelector(".side-nav-menu");
const close_menu = document.querySelector("#close-side-menu");

hamburger.addEventListener("click", function () {
  menu.classList.add("show-side-menu");
});

close_menu.addEventListener("click", function () {
  menu.classList.remove("show-side-menu");
});
