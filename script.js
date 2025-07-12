let recommendations = {};

fetch("recommendations.json")
  .then(response => response.json())
  .then(data => {
    recommendations = data;
  });

function updateMovieList() {
  const lang = document.getElementById("language").value;
  const genre = document.getElementById("genre").value;
  const key = lang + "_" + genre;
  const movieSelect = document.getElementById("movieSelect");
  movieSelect.innerHTML = "";

  if (recommendations[key]) {
    const movies = Object.keys(recommendations[key]);
    movies.forEach(movie => {
      const option = document.createElement("option");
      option.value = movie;
      option.textContent = movie;
      movieSelect.appendChild(option);
    });
  }
}

function getRecommendations() {
  const lang = document.getElementById("language").value;
  const genre = document.getElementById("genre").value;
  const key = lang + "_" + genre;
  const selectedMovies = Array.from(document.getElementById("movieSelect").selectedOptions).map(opt => opt.value);
  const resultList = document.getElementById("resultList");
  resultList.innerHTML = "";

  if (!recommendations[key] || selectedMovies.length === 0) {
    alert("Please select language, genre, and at least one movie.");
    return;
  }

  const allRecs = [];
  selectedMovies.forEach(movie => {
    const recs = recommendations[key][movie] || [];
    allRecs.push(...recs);
  });

  const freq = {};
  allRecs.forEach(rec => {
    freq[rec] = (freq[rec] || 0) + 1;
  });

  const sorted = Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(entry => entry[0]);

  sorted.forEach(rec => {
    const li = document.createElement("li");
    li.textContent = rec;
    resultList.appendChild(li);
  });
}
