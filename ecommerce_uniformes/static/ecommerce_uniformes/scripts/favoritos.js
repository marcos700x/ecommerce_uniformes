document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.eliminar-favorito').forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const varianteId = this.dataset.varianteId;
      const carta = this.closest('.carta-producto');

      fetch(`/toggle-favorito/${varianteId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })
      .then(res => res.json())
      .then(data => {
        if (!data.en_favoritos) {
          carta.remove();
        }
      });
    });
  });
});

// Función para obtener el CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
