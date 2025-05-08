function toggleDone(task_id) {
    fetch(`/toggle/${task_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
}

/* Gestion bouton filtre */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("filter-popup");
    const filter_button = document.getElementById("filter-button");
    const cancel = document.getElementById("filter-button-cancel");

    const register_form = document.getElementById("register-form");
    const register_button = document.getElementById("register-button");
    const register_cancel = document.getElementById("register-button-cancel");
    const login_form = document.getElementById("login-form");
    const login_button = document.getElementById("login-button");
    const login_cancel = document.getElementById("login-button-cancel");

    // Ouvrir / fermer la popup
    filter_button?.addEventListener('click', () => {
        form.classList.toggle('hidden');
    });

    cancel?.addEventListener('click', () => {
        form.classList.add('hidden');
    });

    // Ouvrir / fermer popup inscription-connexion
    register_button?.addEventListener('click', () => {
        register_form.classList.toggle('hidden');
    });

    register_cancel?.addEventListener('click', () => {
        register_form.classList.add('hidden');
    });

    login_button?.addEventListener('click', () => {
        login_form.classList.toggle('hidden');
    });

    login_cancel?.addEventListener('click', () => {
        login_form.classList.add('hidden');
    });

    // Soumettre le filtre (POST avec fetch)
    form?.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch("/filter", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById("task-list").innerHTML = html;
            form.classList.add('hidden'); // Fermer la popup après envoi
        })
        .catch(error => console.error("Erreur lors du filtrage :", error));
    });
});
