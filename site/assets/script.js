// AI Paperwork and Forms Guide — Asdale Dynamics, LLC
// Minimal site behavior: highlight current nav link.

(function () {
  var path = window.location.pathname.split('/').pop() || 'index.html';
  var links = document.querySelectorAll('.chapter-nav a');
  links.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href === path || (path === 'index.html' && href === 'index.html')) {
      link.classList.add('current');
    }
  });
})();
