let jokes = [];

async function loadJokes() {
  const res = await fetch("jokes_100k.json");
  jokes = await res.json();
  showRandomJoke();
}

function showRandomJoke() {
  const joke = jokes[Math.floor(Math.random() * jokes.length)];
  const jokeText = document.getElementById("joke-text");
  const ratingWarning = document.getElementById("rating-warning");
  const revealBtn = document.getElementById("reveal-btn");

  jokeText.textContent = "";
  jokeText.dataset.rating = joke.rating;

  if (joke.rating === "R") {
    ratingWarning.classList.remove("hidden");
    revealBtn.classList.remove("hidden");
    revealBtn.onclick = () => {
      jokeText.textContent = joke.joke;
      revealBtn.classList.add("hidden");
    };
  } else {
    ratingWarning.classList.add("hidden");
    revealBtn.classList.add("hidden");
    jokeText.textContent = joke.joke;
  }
}

window.onload = loadJokes;