async function generateJoke() {
  const res = await fetch('/api/joke');
  const data = await res.json();

  const jokeText = document.getElementById('joke-text');
  const ratingWarning = document.getElementById('rating-warning');
  const revealBtn = document.getElementById('reveal-btn');
  const upvotes = document.getElementById('upvotes');
  const downvotes = document.getElementById('downvotes');

  jokeText.textContent = '';
  upvotes.textContent = data.upvotes;
  downvotes.textContent = data.downvotes;
  jokeText.dataset.jokeId = data.id;

  if (data.rating === 'R') {
    ratingWarning.classList.remove('hidden');
    revealBtn.classList.remove('hidden');
    revealBtn.onclick = () => {
      jokeText.textContent = data.joke;
      revealBtn.classList.add('hidden');
    };
  } else {
    ratingWarning.classList.add('hidden');
    revealBtn.classList.add('hidden');
    jokeText.textContent = data.joke;
  }
}

function vote(type) {
  const jokeText = document.getElementById('joke-text');
  const jokeId = jokeText.dataset.jokeId;
  if (!jokeId) return;

  fetch('/api/vote', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: jokeId, type: type })
  }).then(() => generateJoke());
}

generateJoke();