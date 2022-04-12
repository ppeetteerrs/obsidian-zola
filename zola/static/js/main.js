// Set darkmode
function isDark() {
  return document.body.classList.contains('dark')
}

document.getElementById('mode').addEventListener('click', () => {

  document.body.classList.toggle('dark');

  localStorage.setItem('theme', isDark() ? 'dark' : 'light');

  // Update graph colors if exists
  if (graph) {
    graph.setOptions({
      nodes: {
        color: isDark() ? "#8c8e91" : "#dee2e6",
        font: {
          color: isDark() ? "#c9cdd1" : "#616469",
          strokeColor: isDark() ? "#c9cdd1" : "#616469",
        }
      }
    });
  }

});

// enforce local storage setting but also fallback to user-agent preferences
if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia("(prefers-color-scheme: dark)").matches)) {

  document.body.classList.add('dark');

}
