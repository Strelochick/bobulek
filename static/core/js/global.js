(function () {
  var yearNodes = document.querySelectorAll('[data-current-year]');
  if (!yearNodes.length) return;

  var currentYear = new Date().getFullYear();
  for (var i = 0; i < yearNodes.length; i++) {
    yearNodes[i].textContent = String(currentYear);
  }
})();
