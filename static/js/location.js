function loadDistricts() {
  const region = document.getElementById("region").value;
  const districtSelect = document.getElementById("district");

  // Clear existing options
  districtSelect.innerHTML = '<option value="">Select District</option>';

  if (region) {
    fetch(`/get-districts/${encodeURIComponent(region)}`)
      .then((response) => response.json())
      .then((data) => {
        data.districts.forEach((district) => {
          const option = document.createElement("option");
          option.value = district;
          option.textContent = district;
          districtSelect.appendChild(option);
        });
      });
  }
}
