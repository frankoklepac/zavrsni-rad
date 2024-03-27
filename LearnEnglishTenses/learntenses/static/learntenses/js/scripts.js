let clickedWords = [];
const selectedWordsElement = document.getElementById('selected-words');
document.addEventListener('DOMContentLoaded', () => {

  document.querySelectorAll('.word-button').forEach(button => {
      button.addEventListener('click', () => {
          let word = button.textContent;
          let index = clickedWords.indexOf(word);
          if (index === -1) {
              clickedWords.push(word);
          } else {
              clickedWords.splice(index, 1);
          }
          selectedWordsElement.textContent = "Selected words:" + clickedWords.join(' ');
          console.log(clickedWords); 
      });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
});