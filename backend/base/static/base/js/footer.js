document.getElementById('newsletter-form').onsubmit = function(e) {
  e.preventDefault();
  document.getElementById('popup').style.display = 'flex';
  this.reset();
};

document.getElementById('close-popup').onclick = function() {
  document.getElementById('popup').style.display = 'none';
};