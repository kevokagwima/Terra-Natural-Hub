$(document).ready(function () {
  // Initialize Select2
  $("#disease-select").select2({
    placeholder: "Search and select disease...",
    allowClear: true,
    width: "100%",
  });

  // Handle product selection changes
  $("#disease-select").on("change", function () {
    updateSelectedProductsDisplay();
  });

  // Handle product removal
  $(document).on("click", ".remove-product-btn", function (e) {
    e.preventDefault();
    const productId = $(this).data("id");
    $('#disease-select option[value="' + productId + '"]').prop(
      "selected",
      false
    );
    $("#disease-select").trigger("change");

    // Also remove the product element directly
    $(this).closest(".selected-product").remove();
  });

  // Update the visual display of selected products
  function updateSelectedProductsDisplay() {
    const selectedIds = $("#disease-select").val() || [];
    const container = $("#selected-products-container");

    // First, remove any products that are no longer selected
    $(".selected-product").each(function () {
      const productId = $(this).data("id");
      if (!selectedIds.includes(productId)) {
        $(this).remove();
      }
    });

    // Then add any new selected products that aren't already displayed
    $("#disease-select option:selected").each(function () {
      const productId = $(this).val();
      if ($(`.selected-product[data-id="${productId}"]`).length === 0) {
        const productName = $(this).text().split(" (Ksh")[0];
        const productPrice = $(this)
          .text()
          .match(/Ksh ([\d,]+)/)[1];

        container.append(`
          <div class="selected-product" data-id="${productId}">
            <div class="product-info">
              <div class="product-thumbnail placeholder">
                <i class="fas fa-box-open"></i>
              </div>
              <div class="product-details">
                <span class="product-name">${productName}</span>
                <span class="product-price">Ksh ${productPrice}</span>
              </div>
            </div>
            <button type="button" class="remove-product-btn" data-id="${productId}">
              <i class="fas fa-times"></i>
            </button>
          </div>
        `);
      }
    });
  }
});

// Prescription
$(document).ready(function () {
  // Initialize Select2
  $("#medicine-select").select2({
    placeholder: "Search and select medication...",
    allowClear: true,
    width: "100%",
  });

  // Handle product selection changes
  $("#medicine-select").on("change", function () {
    updateSelectedProductsDisplay();
  });

  // Handle product removal
  $(document).on("click", ".remove-product-btn", function (e) {
    e.preventDefault();
    const productId = $(this).data("id");
    $('#medicine-select option[value="' + productId + '"]').prop(
      "selected",
      false
    );
    $("#medicine-select").trigger("change");

    // Also remove the product element directly
    $(this).closest(".selected-product").remove();
  });

  // Update the visual display of selected products
  function updateSelectedProductsDisplay() {
    const selectedIds = $("#medicine-select").val() || [];
    const container = $("#selected-products-container");

    // First, remove any products that are no longer selected
    $(".selected-product").each(function () {
      const productId = $(this).data("id");
      if (!selectedIds.includes(productId)) {
        $(this).remove();
      }
    });

    // Then add any new selected products that aren't already displayed
    $("#medicine-select option:selected").each(function () {
      const productId = $(this).val();
      if ($(`.selected-product[data-id="${productId}"]`).length === 0) {
        const productName = $(this).text().split(" (Ksh")[0];
        const productPrice = $(this)
          .text()
          .match(/Ksh ([\d,]+)/)[1];

        container.append(`
          <div class="selected-product" data-id="${productId}">
            <div class="product-info">
              <div class="product-thumbnail placeholder">
                <i class="fas fa-box-open"></i>
              </div>
              <div class="product-details">
                <span class="product-name">${productName}</span>
                <span class="product-price">Ksh ${productPrice}</span>
              </div>
            </div>
            <button type="button" class="remove-product-btn" data-id="${productId}">
              <i class="fas fa-times"></i>
            </button>
          </div>
        `);
      }
    });
  }
});

document.querySelectorAll(".accordion-header").forEach((header) => {
  header.addEventListener("click", () => {
    const content = header.nextElementSibling;
    const isVisible = content.style.display === "block";

    // Toggle display
    content.style.display = isVisible ? "none" : "block";
  });
});
