const menu = document.querySelector(".nav__menu");
const menuSidebar = document.querySelector(".nav__menu-sidebar");
let isMenuOpend = false;

menu.addEventListener("mouseover", () => {
  console.log("mouse is over");
  menuSidebar.style.display = "block";
});

menu.addEventListener("mouseout", () => {
  console.log("mouse is out");
  menuSidebar.style.display = "none";
});
