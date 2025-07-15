document.addEventListener("DOMContentLoaded", function () {
  // Modal elements
  const modal = document.getElementById("branchModal");
  const addBtn = document.getElementById("addBranchBtn");
  const closeBtn = document.querySelector(".close");
  const cancelBtn = document.getElementById("cancelBtn");
  const statusToggle = document.getElementById("branchStatus");
  const statusLabel = document.getElementById("statusLabel");
  const branchForm = document.getElementById("branchForm");

  // Toggle modal
  addBtn.addEventListener("click", () => (modal.style.display = "flex"));
  closeBtn.addEventListener("click", () => (modal.style.display = "none"));
  cancelBtn.addEventListener("click", () => (modal.style.display = "none"));

  // Close modal when clicking outside
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });

  // Toggle status label
  statusToggle.addEventListener("change", function () {
    statusLabel.textContent = this.checked ? "Active" : "Inactive";
  });
});
