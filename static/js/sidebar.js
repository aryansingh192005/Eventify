document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll(".sidebar-section");

    sections.forEach(section => {

        const next = section.nextElementSibling;

        if (
            next &&
            next.classList.contains("sidebar-link") &&
            next.classList.contains("active")
        ) {

            section.style.color = "#2563eb";

        }

    });

});

