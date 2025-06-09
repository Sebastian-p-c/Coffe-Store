document.addEventListener('DOMContentLoaded', () => {
    // Seleccionamos el elemento header_texto
    const headerText = document.querySelector('.header_texto');

    // Si el elemento no existe, no ejecutamos nada
    if (!headerText) return;

    // Opciones del IntersectionObserver para la animación de desenfoque
    const options = {
        root: null, // Usamos el viewport como raíz
        threshold: 0.1, // La animación se dispara cuando al menos el 10% del artículo es visible
    };

    // Función que se ejecuta cuando el header_texto entra en el viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Cuando header_texto entra en el viewport, agregar la clase 'visible'
                headerText.classList.add('visible');
            } else {
                // Cuando header_texto sale del viewport, remover la clase 'visible'
                headerText.classList.remove('visible');
            }
        });
    }, options);

    // Iniciamos la observación
    observer.observe(headerText);
});