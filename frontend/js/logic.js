
const mapData = [
    {
      id: 1,
      name: "Restaurant A",
      lat: 40.7128,
      lng: -74.0060,
      borough: "Manhattan",
      cuisine: "Italian",
      inspection_date: "2025-03-01T00:00:00"
    },
    {
      id: 2,
      name: "Restaurant B",
      lat: 40.6782,
      lng: -73.9442,
      borough: "Brooklyn",
      cuisine: "Chinese",
      inspection_date: "2025-03-02T00:00:00"
    }
  ];

  const topCuisinesData = [
    { cuisine: "Italian", count: 30 },
    { cuisine: "Chinese", count: 20 },
    { cuisine: "Mexican", count: 15 }
  ];

  const cuisineDistributionData = [
    { cuisine: "Italian", count: 50, percentage: 30 },
    { cuisine: "Chinese", count: 40, percentage: 24 },
    { cuisine: "Mexican", count: 35, percentage: 21 },
    { cuisine: "Indian", count: 25, percentage: 15 },
    { cuisine: "Other", count: 10, percentage: 10 }
  ];

  const boroughSummaryData = [
    { borough: "Manhattan", restaurant_count: 100, average_rating: 4.1, restaurants_per_capita: 0.012 },
    { borough: "Brooklyn", restaurant_count: 150, average_rating: 4.0, restaurants_per_capita: 0.010 },
    { borough: "Bronx", restaurant_count: 80, average_rating: 3.8, restaurants_per_capita: 0.008 },
    { borough: "Queens", restaurant_count: 120, average_rating: 3.9, restaurants_per_capita: 0.009 },
    { borough: "Staten Island", restaurant_count: 40, average_rating: 4.2, restaurants_per_capita: 0.005 }
  ];

  // Init Leaflet Map
  const map = L.map('map').setView([40.7128, -74.0060], 11);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
  mapData.forEach(loc => {
    L.marker([loc.lat, loc.lng])
      .addTo(map)
      .bindPopup(`<b>${loc.name}</b><br>Borough: ${loc.borough}<br>Cuisine: ${loc.cuisine}<br>Inspected: ${new Date(loc.inspection_date).toLocaleDateString()}`);
  });

  // Bar Chart
  const barCtx = document.getElementById('barChart').getContext('2d');
  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: topCuisinesData.map(item => item.cuisine),
      datasets: [{
        label: 'Top Cuisines by Count',
        data: topCuisinesData.map(item => item.count),
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Pie Chart
  const pieCtx = document.getElementById('pieChart').getContext('2d');
  new Chart(pieCtx, {
    type: 'pie',
    data: {
      labels: cuisineDistributionData.map(item => item.cuisine),
      datasets: [{
        data: cuisineDistributionData.map(item => item.percentage),
      }]
    },
    options: { responsive: true }
  });

  // Table
  const tableBody = document.getElementById("boroughTableBody");
  boroughSummaryData.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.borough}</td>
      <td>${row.restaurant_count}</td>
      <td>${row.average_rating}</td>
      <td>${row.restaurants_per_capita}</td>
    `;
    tableBody.appendChild(tr);
  });


