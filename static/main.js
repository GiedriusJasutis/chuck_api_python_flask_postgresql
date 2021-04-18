const getJoke = document.querySelector('#get-joke-handler');
const joke = document.querySelector('#joke');
const jokeInput = document.querySelector('#joke-input');

if (getJoke !== null) {
  // update hidden input when page is loaded
  document.addEventListener('DOMContentLoaded', function () {
    jokeInput.value = joke.textContent;
  });

  // save joke to list
  getJoke.addEventListener('click', () => {
    fetch('https://api.chucknorris.io/jokes/random')
      .then((response) => response.json())
      .then((data) => {
        joke.textContent = data.value;
        jokeInput.value = data.value;
      });
  });
}
