document.addEventListener("DOMContentLoaded", function () {
  // Tab switching functionality
  const tabs = document.querySelectorAll(".med-tab");
  const tabContents = document.querySelectorAll(".results-card");

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

  // Diagnosis Toggle Functionality
  const diagnosisToggles = document.querySelectorAll(".diagnosis-toggle");
  let currentDiagnosisOpen = null;

  diagnosisToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const details = document.getElementById(targetId);
      const icon = this.querySelector("i");

      // If clicking the currently open section, close it
      if (currentDiagnosisOpen === targetId) {
        details.classList.remove("active");
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
        currentDiagnosisOpen = null;
        return;
      }

      // Close the previously open section if exists
      if (currentDiagnosisOpen) {
        const prevDetails = document.getElementById(currentDiagnosisOpen);
        const prevButton = document.querySelector(
          `.diagnosis-toggle[data-target="${currentDiagnosisOpen}"] i`
        );
        if (prevDetails) prevDetails.classList.remove("active");
        if (prevButton) {
          prevButton.classList.remove("fa-chevron-up");
          prevButton.classList.add("fa-chevron-down");
        }
      }

      // Open the clicked section
      details.classList.add("active");
      icon.classList.remove("fa-chevron-down");
      icon.classList.add("fa-chevron-up");
      currentDiagnosisOpen = targetId;
    });
  });

  // Prescription Toggle Functionality
  const prescriptionToggles = document.querySelectorAll(".prescription-toggle");
  let currentPrescriptionOpen = null;

  prescriptionToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const details = document.getElementById(targetId);
      const icon = this.querySelector("i");

      // If clicking the currently open section, close it
      if (currentPrescriptionOpen === targetId) {
        details.classList.remove("active");
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
        currentPrescriptionOpen = null;
        return;
      }

      // Close the previously open section if exists
      if (currentPrescriptionOpen) {
        const prevDetails = document.getElementById(currentPrescriptionOpen);
        const prevButton = document.querySelector(
          `.prescription-toggle[data-target="${currentPrescriptionOpen}"] i`
        );
        if (prevDetails) prevDetails.classList.remove("active");
        if (prevButton) {
          prevButton.classList.remove("fa-chevron-up");
          prevButton.classList.add("fa-chevron-down");
        }
      }

      // Open the clicked section
      details.classList.add("active");
      icon.classList.remove("fa-chevron-down");
      icon.classList.add("fa-chevron-up");
      currentPrescriptionOpen = targetId;
    });
  });
});
