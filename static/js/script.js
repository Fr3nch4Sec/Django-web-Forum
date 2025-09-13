document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const html = document.documentElement;

    // Charger l'état initial du mode sombre depuis le localStorage
    const isDarkMode = localStorage.getItem('dark_mode') === 'true';
    if (isDarkMode) {
        html.classList.add('dark');
        toggleButton.textContent = 'Mode Clair';
    } else {
        html.classList.remove('dark');
        toggleButton.textContent = 'Mode Sombre';
    }

    // Gérer le clic sur le bouton
    toggleButton.addEventListener('click', () => {
        const darkMode = !html.classList.contains('dark');
        html.classList.toggle('dark');
        toggleButton.textContent = darkMode ? 'Mode Clair' : 'Mode Sombre';

        // Envoyer l'état à la vue Django
        fetch('/toggle-dark-mode/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ dark_mode: darkMode })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    localStorage.setItem('dark_mode', darkMode);
                }
            })
            .catch(error => console.error('Erreur:', error));
    });
});