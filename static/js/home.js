const maintabs = document.querySelectorAll(".nav-item");
const maintabContents = document.querySelectorAll(".tabContent");

maintabs.forEach((maintab) => {
  maintab.addEventListener("click", () => {
    // Remove active class from all tabs and contents
    maintabs.forEach((t) => t.classList.remove("active"));
    maintabContents.forEach((x) => x.classList.remove("active"));

    // Add active class to clicked tab and corresponding content
    maintab.classList.add("active");
    const maintabId = maintab.getAttribute("data-tab");
    document.getElementById(maintabId).classList.add("active");
  });
});

const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    // Remove active class from all tabs and contents
    tabs.forEach((t) => t.classList.remove("active"));
    tabContents.forEach((c) => c.classList.remove("active"));

    // Add active class to clicked tab and corresponding content
    tab.classList.add("active");
    const tabId = tab.getAttribute("data-tab");
    document.getElementById(tabId).classList.add("active");
  });
});

const medicaltabs = document.querySelectorAll(".med-tab");
const medical_table = document.querySelectorAll(".medical-data-table");

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
