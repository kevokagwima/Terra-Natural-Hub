let currentlyOpen = null;

document.querySelectorAll(".toggle-details").forEach((button) => {
  button.addEventListener("click", (e) => {
    const targetId = button.getAttribute("data-target");
    const details = document.getElementById(targetId);
    const icon = button.querySelector("i");

    // If clicking the currently open section, close it
    if (currentlyOpen === targetId) {
      details.classList.remove("active");
      icon.classList.remove("fa-chevron-up");
      icon.classList.add("fa-chevron-down");
      currentlyOpen = null;
      return;
    }

    // Close the previously open section if exists
    if (currentlyOpen) {
      const prevDetails = document.getElementById(currentlyOpen);
      const prevButton = document.querySelector(
        `.toggle-details[data-target="${currentlyOpen}"] i`
      );
      prevDetails.classList.remove("active");
      prevButton.classList.remove("fa-chevron-up");
      prevButton.classList.add("fa-chevron-down");
    }

    // Open the clicked section
    details.classList.add("active");
    icon.classList.remove("fa-chevron-down");
    icon.classList.add("fa-chevron-up");
    currentlyOpen = targetId;
  });
});

const medicaltabs = document.querySelectorAll(".med-tab");
const medical_table = document.querySelectorAll(".results-card");

medicaltabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    // Remove active class from all tabs and contents
    medicaltabs.forEach((t) => t.classList.remove("active"));
    medical_table.forEach((c) => c.classList.remove("active"));

    // Add active class to clicked tab and corresponding content
    tab.classList.add("active");
    const tabId = tab.getAttribute("data-tab");
    document.getElementById(tabId).classList.add("active");
  });
});
