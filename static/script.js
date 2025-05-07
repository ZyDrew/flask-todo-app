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

    // Ouvrir / fermer la popup
    filter_button?.addEventListener('click', () => {
        form.classList.toggle('hidden');
    });

    cancel?.addEventListener('click', () => {
        form.classList.add('hidden');
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
