const searchInput = document.getElementById("patient-search");
const searchBox = document.querySelector(".search-box");

function debounce(func, delay) {
  let timeout;
  return function (...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), delay);
  };
}

function fetchPatient() {
  const searchInputValue = searchInput.value;

  if (!searchInputValue) {
    searchBox.style.display = "none";
    return;
  }

  fetch("/find-patient/" + searchInputValue)
    .then((response) => response.json())
    .then((patient) => {
      displayPatient(patient);
    });
}

function displayPatient(patient) {
  if (patient.length === 0) {
    searchBox.innerHTML = "No patient found";
  } else {
    searchBox.innerHTML = "";
    patient.forEach((patient) => {
      const searchResult = document.createElement("div");
      searchResult.className = "search-result";
      const searchResultlink = document.createElement("a");
      const searchResultText = document.createElement("p");
      const searchResultText2 = document.createElement("p");
      const searchResultText3 = document.createElement("p");
      searchResultText.className = "resulttext";

      searchResultlink.href = `/profile/patient/${patient.unique_id}`;
      searchResultText.innerHTML = `${patient.name}`;
      searchResultText2.innerHTML = `PT - ${patient.unique_id}`;
      searchResultText3.innerHTML = `${patient.gender}`;

      searchResult.appendChild(searchResultText);
      searchResult.appendChild(searchResultText2);
      searchResult.appendChild(searchResultText3);
      searchResultlink.appendChild(searchResult);
      searchBox.appendChild(searchResultlink);

      searchBox.style.display = "grid";
    });
  }
}

searchInput.addEventListener("keyup", debounce(fetchPatient, 300));
