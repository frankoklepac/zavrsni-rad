document.getElementById('solve-tasks').addEventListener('click', function(event) {
  event.preventDefault();
  var tasks = document.getElementById('tasks');
  tasks.style.display = tasks.style.display === 'none' ? 'block' : 'none';
});

const sentenceField = document.getElementById('id_form-sentence');
const wordsField = document.getElementById('id_form-words');
const correctWordsField = document.getElementById('id_form-correct_words');

function autoExpand(element) {
  element.style.height = 'inherit';
  const computed = window.getComputedStyle(element);
  const height = parseInt(computed.getPropertyValue('border-top-width'), 10)
                 + parseInt(computed.getPropertyValue('border-bottom-width'), 10)
                 + element.scrollHeight;
  
  element.style.height = height + 'px';
}

sentenceField.addEventListener('input', () => autoExpand(sentenceField));
wordsField.addEventListener('input', () => autoExpand(wordsField));
correctWordsField.addEventListener('input', () => autoExpand(correctWordsField));

