document.getElementById('solve-tasks').addEventListener('click', function(event) {
  event.preventDefault();
  var tasks = document.getElementById('tasks');
  tasks.style.display = tasks.style.display === 'none' ? 'block' : 'none';
});