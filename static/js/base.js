function openTab(event, tabName) {
  // Hide all tab contents
  const tabContents = document.querySelectorAll(".tab-content");
  tabContents.forEach((content) => {
    content.classList.remove("active");
  });

  // Remove active class from all buttons
  const tabButtons = document.querySelectorAll(".menu-item");
  tabButtons.forEach((button) => {
    button.classList.remove("active");
  });

  // Show the selected tab content and add active class to the button
  document.getElementById(tabName).classList.add("active");
  event.currentTarget.classList.add("active");
}

function toggleMenu() {
  const menu = document.getElementById("mobile-menu");
  menu.classList.toggle("show");
}

// function openTabTwo(event, tabName) {
//   // Hide all tab contents
//   const tabContents = document.querySelectorAll(".tab-content");
//   tabContents.forEach((content) => {
//     content.classList.remove("active");
//   });

//   // Remove active class from all buttons
//   const tabButtons = document.querySelectorAll(".menu-item-2");
//   tabButtons.forEach((button) => {
//     button.classList.remove("active");
//   });

//   // Show the selected tab content and add active class to the button
//   document.getElementById(tabName).classList.add("active");
//   event.currentTarget.classList.add("active");
// }

// function toggleMenu() {
//   const menu = document.getElementById("mobile-menu");
//   menu.classList.toggle("show");
// }