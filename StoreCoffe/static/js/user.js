document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const loginLink = document.getElementById('login-link');
    const usuarioInfo = document.getElementById('usuario-info');
    const nombreUsuario = document.getElementById('nombre-usuario');
    const menu = document.querySelector('.usuario-menu');

    if (token && nombreUsuario && loginLink && usuarioInfo) {
        fetch('/api/usuarios/me/', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('No autorizado');
            return response.json();
        })
        .then(data => {
            nombreUsuario.textContent = data.username;
            loginLink.style.display = 'none';
            usuarioInfo.style.display = 'inline-block';
        })
        .catch(error => {
            console.error('Error al obtener los datos del usuario', error);
            localStorage.removeItem('access_token');
            usuarioInfo.style.display = 'none';
            loginLink.style.display = 'inline-block';
        });
    }

    usuarioInfo?.addEventListener('click', (event) => {
        event.stopPropagation();
        menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
    });

    document.addEventListener('click', (event) => {
        if (!usuarioInfo?.contains(event.target)) {
            menu.style.display = 'none';
        }
    });

    document.getElementById('update-password')?.addEventListener('click', (e) => {
        e.stopPropagation();
        const nuevaClave = prompt('Introduce tu nueva contraseña:');
        if (nuevaClave) {
            fetch('/api/usuarios/me/cambiar_contrasena/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nueva_clave: nuevaClave })
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje) {
                    alert('Contraseña actualizada correctamente');
                } else {
                    alert('Error al actualizar la contraseña');
                }
            })
            .catch(error => {
                console.error('Error al cambiar la contraseña', error);
            });
        }
    });

    document.getElementById('delete-account')?.addEventListener('click', (e) => {
        e.stopPropagation();
        if (confirm('¿Seguro que quieres eliminar tu cuenta?')) {
            fetch('/api/usuarios/me/eliminar_cuenta/', {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            })
            .then(response => {
                if (response.ok) {
                    alert('Tu cuenta ha sido eliminada.');
                    localStorage.removeItem('access_token');
                    window.location.href = '/';
                } else {
                    alert('Hubo un error al eliminar tu cuenta.');
                }
            })
            .catch(error => {
                console.error('Error al eliminar la cuenta', error);
            });
        }
    });

    document.getElementById('logout')?.addEventListener('click', (e) => {
        e.stopPropagation();
        localStorage.removeItem('access_token');
        alert('Sesión cerrada correctamente.');
        window.location.href = '/';
    });
});
