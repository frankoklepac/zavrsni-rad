let clickedWords = [];

document.querySelectorAll('.word-button').forEach(button => {
  button.addEventListener('click', () => {
    let word = button.textContent;
    let index = clickedWords.indexOf(word);
    if (index === -1) {
      clickedWords.push(word);
    } else {
      clickedWords.splice(index, 1);
    }
    console.log(clickedWords);
  });
});