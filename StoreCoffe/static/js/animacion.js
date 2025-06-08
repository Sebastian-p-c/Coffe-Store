// Seleccionamos el artículo que queremos animar
const articles = document.querySelectorAll('article.entrada');

// Opciones del IntersectionObserver
const options = {
    root: null, // Usamos el viewport como raíz
    threshold: 0.1, // La animación se dispara cuando al menos el 10% del artículo es visible
};

// Función que se ejecuta cuando el artículo entra en el viewport
const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        // Si el artículo está visible, agregar la clase para la animación
        if (entry.isIntersecting) {
            entry.target.classList.add('article-visible');
        } else {
            // Si el artículo ya no está visible, lo regresamos a su posición inicial
            entry.target.classList.remove('article-visible');
        }
    });
}, options);

// Observar todos los artículos
articles.forEach(article => {
    article.classList.add('article-animado');
    observer.observe(article);
});