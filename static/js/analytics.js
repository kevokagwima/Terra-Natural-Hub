const diseasesCtx = document.getElementById("diseasesChart").getContext("2d");
const medicationsCtx = document
  .getElementById("medicationsChart")
  .getContext("2d");

const diseasesChart = new Chart(diseasesCtx, {
  type: "bar",
  data: {
    labels: ["Hypertension", "Diabetes", "Asthma", "Arthritis", "Anemia"],
    datasets: [
      {
        label: "Diagnoses",
        data: [42, 28, 19, 15, 12],
        backgroundColor: "#ef233c",
        borderColor: "#ef233c",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 5,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

const medicationsChart = new Chart(medicationsCtx, {
  type: "bar",
  data: {
    labels: [
      "Lisinopril",
      "Metformin",
      "Amoxicillin",
      "Atorvastatin",
      "Albuterol",
    ],
    datasets: [
      {
        label: "Prescriptions",
        data: [58, 42, 37, 29, 25],
        backgroundColor: "#4cc9f0",
        borderColor: "#4cc9f0",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 5,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

// Filter functionality
document.getElementById("apply-filter").addEventListener("click", function () {
  const month = document.getElementById("month").value;
  const year = document.getElementById("year").value;

  // Here you would typically make an AJAX call to your backend
  // For this example, we'll just simulate filtered data
  simulateFilteredData(month, year);
});

function simulateFilteredData(month, year) {
  // Simulate API call delay
  setTimeout(() => {
    // Example filtered data - in a real app, this would come from your backend
    let diseasesData, medicationsData;

    if (month === "all") {
      diseasesData = [
        { name: "Hypertension", count: 42 },
        { name: "Diabetes Mellitus", count: 28 },
        { name: "Asthma", count: 19 },
      ];

      medicationsData = [
        { name: "Lisinopril", count: 58 },
        { name: "Metformin", count: 42 },
        { name: "Amoxicillin", count: 37 },
      ];
    } else {
      // Simulate monthly data
      diseasesData = [
        { name: "Hypertension", count: Math.floor(Math.random() * 10) + 5 },
        { name: "Diabetes Mellitus", count: Math.floor(Math.random() * 8) + 3 },
        { name: "Asthma", count: Math.floor(Math.random() * 6) + 2 },
      ];

      medicationsData = [
        { name: "Lisinopril", count: Math.floor(Math.random() * 12) + 6 },
        { name: "Metformin", count: Math.floor(Math.random() * 10) + 4 },
        { name: "Amoxicillin", count: Math.floor(Math.random() * 8) + 3 },
      ];
    }

    updateUI(diseasesData, medicationsData);
  }, 500);
}

function updateUI(diseases, medications) {
  // Update diseases list
  const diseasesContainer = document.getElementById("diseases-container");
  diseasesContainer.innerHTML = "";

  diseases.forEach((disease, index) => {
    const item = document.createElement("div");
    item.className = "stat-item";
    item.innerHTML = `
                    <div class="stat-info">
                        <span>${index + 1}</span>
                        <span>${disease.name}</span>
                    </div>
                    <span class="stat-count">${disease.count} cases</span>
                `;
    diseasesContainer.appendChild(item);
  });

  // Update medications list
  const medicationsContainer = document.getElementById("medications-container");
  medicationsContainer.innerHTML = "";

  medications.forEach((medication, index) => {
    const item = document.createElement("div");
    item.className = "stat-item";
    item.innerHTML = `
                    <div class="stat-info">
                        <span>${index + 1}</span>
                        <span>${medication.name}</span>
                    </div>
                    <span class="stat-count">${
                      medication.count
                    } prescriptions</span>
                `;
    medicationsContainer.appendChild(item);
  });

  // Update charts
  diseasesChart.data.datasets[0].data = diseases.map((d) => d.count);
  diseasesChart.data.labels = diseases.map((d) => d.name);
  diseasesChart.update();

  medicationsChart.data.datasets[0].data = medications.map((m) => m.count);
  medicationsChart.data.labels = medications.map((m) => m.name);
  medicationsChart.update();
}
