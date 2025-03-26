

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

// ==================
// Leaflet Map Setup
// ==================

const map = L.map('map').setView([40.7128, -74.0060], 11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

mapData.forEach(loc => {
  L.marker([loc.lat, loc.lng])
    .addTo(map)
    .bindPopup(`<b>${loc.name}</b><br>Borough: ${loc.borough}<br>Cuisine: ${loc.cuisine}<br>Inspected: ${new Date(loc.inspection_date).toLocaleDateString()}`);
});

// ==================
// Bar Chart (Plotly)
// ==================

const boroughCuisineData = {
  Manhattan: [
    { cuisine: 'Italian', count: 120 },
    { cuisine: 'Chinese', count: 95 },
    { cuisine: 'American', count: 80 }
  ],
  Brooklyn: [
    { cuisine: 'Caribbean', count: 110 },
    { cuisine: 'Mexican', count: 90 },
    { cuisine: 'American', count: 85 }
  ],
  Queens: [
    { cuisine: 'Indian', count: 100 },
    { cuisine: 'Chinese', count: 95 },
    { cuisine: 'Korean', count: 80 }
  ]
};

// Extract borough names
const boroughs = Object.keys(boroughCuisineData);

// Create initial trace (default: Manhattan)
const defaultBorough = boroughs[0];
const initialData = boroughCuisineData[defaultBorough];

const barTrace = {
  x: initialData.map(item => item.cuisine),
  y: initialData.map(item => item.count),
  type: 'bar',
  marker: {
    color: 'rgba(55,128,191,0.7)',
    line: { color: 'rgba(55,128,191,1.0)', width: 2 }
  }
};

// Create dropdown menu options
const updatemenus = [
  {
    buttons: boroughs.map(borough => ({
      method: 'update',
      label: borough,
      args: [
        [{
          x: [boroughCuisineData[borough].map(item => item.cuisine)],
          y: [boroughCuisineData[borough].map(item => item.count)]
        }],
        { title: `Top Cuisines in ${borough}` }
      ]
    })),
    direction: 'down',
    showactive: true,
    x: 0,
    xanchor: 'left',
    y: 1.15,
    yanchor: 'top'
  }
];

const barLayout = {
  title: `Top Cuisines in ${defaultBorough}`,
  xaxis: { title: 'Cuisine' },
  yaxis: { title: 'Count' },
  updatemenus: updatemenus
};

Plotly.newPlot('barChart', [barTrace], barLayout);

// ==================
// Pie Chart (Plotly)
// ==================

const pieTrace = {
  labels: cuisineDistributionData.map(item => item.cuisine),
  values: cuisineDistributionData.map(item => item.percentage),
  type: 'pie',
  textinfo: 'label+percent',
  hoverinfo: 'label+percent+value',
  domain: {
    x: [0, 1], // full width
    y: [0, 1]  // full height
  }
};

const pieLayout = {
  title: 'Cuisine Distribution in NYC',
  height: 400, // Increase overall chart height
  width: 400,  // Increase overall chart width
  margin: { t: 40, l: 40, r: 40, b: 40 } 
};

Plotly.newPlot('pieChart', [pieTrace], pieLayout);



// ==================
// Borough Summary Table
// ==================

const tableBody = document.getElementById("boroughTableBody");

boroughSummaryData.forEach(row => {
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${row.borough}</td>
    <td>${row.restaurant_count}</td>
    <td>${row.average_rating.toFixed(1)}</td>
    <td>${row.restaurants_per_capita.toFixed(3)}</td>
  `;
  tableBody.appendChild(tr);
});


