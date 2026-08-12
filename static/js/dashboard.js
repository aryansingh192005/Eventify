/* ==========================================================
   EVENTIFY DASHBOARD JAVASCRIPT
========================================================== */

document.addEventListener("DOMContentLoaded", function () {


    /* ======================================================
       ELEMENTS
    ====================================================== */

    const layout = document.getElementById("dashboardLayout");
    const sidebarToggle = document.getElementById("sidebarToggle");


    /* ======================================================
       BOOTSTRAP TOOLTIPS
    ====================================================== */

    if (window.bootstrap) {

        document
            .querySelectorAll('[data-bs-toggle="tooltip"]')
            .forEach(function (element) {

                new bootstrap.Tooltip(element);

            });

    }


    /* ======================================================
       SIDEBAR TOGGLE
    ====================================================== */

    if (layout && sidebarToggle) {

        if (
            localStorage.getItem("sidebarCollapsed") === "true"
        ) {

            layout.classList.add("sidebar-collapsed");

        }


        sidebarToggle.addEventListener("click", function () {

            layout.classList.toggle("sidebar-collapsed");

            localStorage.setItem(
                "sidebarCollapsed",
                layout.classList.contains("sidebar-collapsed")
            );

        });

    }


    /* ======================================================
       AUTO DISMISS ALERTS
    ====================================================== */

    document
        .querySelectorAll(".alert")
        .forEach(function (alert) {

            setTimeout(function () {

                alert.classList.add("fade");

                setTimeout(function () {

                    alert.remove();

                }, 300);

            }, 4000);

        });


    /* ======================================================
       BUTTON RIPPLE
    ====================================================== */

    document
        .querySelectorAll(".btn")
        .forEach(function (button) {

            button.addEventListener("click", function (event) {

                const ripple = document.createElement("span");

                const rect = this.getBoundingClientRect();

                const size = Math.max(
                    rect.width,
                    rect.height
                );

                ripple.style.width = size + "px";
                ripple.style.height = size + "px";

                ripple.style.left =
                    event.clientX -
                    rect.left -
                    size / 2 +
                    "px";

                ripple.style.top =
                    event.clientY -
                    rect.top -
                    size / 2 +
                    "px";

                ripple.style.position = "absolute";
                ripple.style.borderRadius = "50%";
                ripple.style.background =
                    "rgba(255,255,255,.35)";
                ripple.style.transform = "scale(0)";
                ripple.style.animation =
                    "ripple .6s linear";
                ripple.style.pointerEvents = "none";

                this.appendChild(ripple);

                setTimeout(function () {

                    ripple.remove();

                }, 600);

            });

        });


    /* ======================================================
       COUNTER ANIMATION
    ====================================================== */

    document
        .querySelectorAll(".stats-number")
        .forEach(function (counter) {

            const text =
                counter.innerText.trim();

            const currency =
                text.includes("₹");

            const target =
                parseInt(
                    text.replace(/[^\d]/g, "")
                ) || 0;

            if (target === 0) {
                return;
            }

            let current = 0;

            const step =
                Math.max(
                    1,
                    Math.ceil(target / 60)
                );


            function animate() {

                current += step;

                if (current > target) {
                    current = target;
                }

                counter.innerText = currency
                    ? "₹" + current.toLocaleString()
                    : current.toLocaleString();


                if (current < target) {

                    requestAnimationFrame(
                        animate
                    );

                }

            }


            animate();

        });


    /* ======================================================
       CARD APPEAR ANIMATION
    ====================================================== */

    document
        .querySelectorAll(
            ".card, .stats-card, .dashboard-card"
        )
        .forEach(function (card, index) {

            card.style.opacity = "0";
            card.style.transform =
                "translateY(25px)";

            setTimeout(function () {

                card.style.transition =
                    ".45s ease";

                card.style.opacity = "1";

                card.style.transform =
                    "translateY(0)";

            }, index * 60);

        });


    /* ======================================================
       IMAGE LAZY LOADING
    ====================================================== */

    document
        .querySelectorAll("img")
        .forEach(function (image) {

            image.loading = "lazy";

        });


    /* ======================================================
       DASHBOARD SEARCH
    ====================================================== */

    const search =
        document.getElementById(
            "dashboardSearch"
        );


    if (search) {

        search.addEventListener(
            "keyup",
            function () {

                const value =
                    this.value.toLowerCase();

                document
                    .querySelectorAll("tbody tr")
                    .forEach(function (row) {

                        row.style.display =
                            row.innerText
                                .toLowerCase()
                                .includes(value)
                                ? ""
                                : "none";

                    });

            }
        );

    }


    /* ======================================================
       BACK TO TOP
    ====================================================== */

    const topButton =
        document.querySelector(
            ".scroll-top"
        );


    if (topButton) {

        window.addEventListener(
            "scroll",
            function () {

                topButton.style.display =
                    window.scrollY > 250
                        ? "flex"
                        : "none";

            }
        );

    }


    /* ======================================================
       FORM LOADING
    ====================================================== */

    document
        .querySelectorAll("form")
        .forEach(function (form) {

            form.addEventListener(
                "submit",
                function () {

                    const submit =
                        form.querySelector(
                            'button[type="submit"]'
                        );


                    if (submit) {

                        submit.disabled = true;

                        submit.dataset.original =
                            submit.innerHTML;

                        submit.innerHTML = `
                            <span class="spinner-border spinner-border-sm me-2"></span>
                            Processing...
                        `;

                    }

                }
            );

        });


});


/* ==========================================================
   RIPPLE CSS
========================================================== */

const rippleStyle =
    document.createElement("style");

rippleStyle.innerHTML = `

@keyframes ripple {

    from {

        transform: scale(0);
        opacity: .6;

    }

    to {

        transform: scale(4);
        opacity: 0;

    }

}

.btn {

    overflow: hidden;
    position: relative;

}

`;

document.head.appendChild(rippleStyle);


/* ==========================================================
   EVENTIFY CUSTOMIZATION SYSTEM
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        const panel =
            document.getElementById(
                "customizationPanel"
            );

        const overlay =
            document.getElementById(
                "customizationOverlay"
            );

        const openButton =
            document.getElementById(
                "customizeToggle"
            );

        const closeButton =
            document.getElementById(
                "customizationClose"
            );

        const resetButton =
            document.getElementById(
                "resetCustomization"
            );


        /*
         * If customization HTML is not present,
         * don't do anything.
         */

        if (
            !panel ||
            !overlay ||
            !openButton
        ) {

            return;

        }


        /* ==================================================
           DEFAULTS
        ================================================== */

        const defaults = {

            theme: "light",

            color: "indigo",

            sidebar: "expanded",

            density: "comfortable",

            font: "Poppins"

        };


        /* ==================================================
           COLORS
        ================================================== */

        const colors = {

            indigo: {
                primary: "#4f46e5",
                dark: "#4338ca"
            },

            blue: {
                primary: "#2563eb",
                dark: "#1d4ed8"
            },

            purple: {
                primary: "#7c3aed",
                dark: "#6d28d9"
            },

            green: {
                primary: "#16a34a",
                dark: "#15803d"
            },

            orange: {
                primary: "#ea580c",
                dark: "#c2410c"
            },

            red: {
                primary: "#dc2626",
                dark: "#b91c1c"
            },

            pink: {
                primary: "#db2777",
                dark: "#be185d"
            }

        };

        /* ==================================================
   THEME PRESETS
================================================== */

const presets = {

    default: {
        color: "indigo"
    },

    ocean: {
        color: "blue"
    },

    emerald: {
        color: "green"
    },

    sunset: {
        color: "orange"
    },

    rose: {
        color: "pink"
    }

};


        /* ==================================================
           LOAD SETTINGS
        ================================================== */

        let settings = {

            ...defaults

        };


        try {

            const saved =
                localStorage.getItem(
                    "eventifyCustomization"
                );


            if (saved) {

                settings = {

                    ...defaults,

                    ...JSON.parse(saved)

                };

            }

        } catch (error) {

            console.warn(
                "Eventify customization settings could not be loaded."
            );

        }


        /* ==================================================
           SAVE
        ================================================== */

        function saveSettings() {

            localStorage.setItem(
                "eventifyCustomization",
                JSON.stringify(settings)
            );

        }


        /* ==================================================
           OPEN PANEL
        ================================================== */

        function openCustomization() {

            panel.classList.add("active");

            overlay.classList.add("active");

            document.body.style.overflow =
                "hidden";

        }


        /* ==================================================
           CLOSE PANEL
        ================================================== */

        function closeCustomization() {

            panel.classList.remove("active");

            overlay.classList.remove("active");

            document.body.style.overflow =
                "";

        }


        openButton.addEventListener(
            "click",
            openCustomization
        );


        if (closeButton) {

            closeButton.addEventListener(
                "click",
                closeCustomization
            );

        }


        overlay.addEventListener(
            "click",
            closeCustomization
        );


        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape" &&
                    panel.classList.contains("active")
                ) {

                    closeCustomization();

                }

            }
        );


        /* ==================================================
           COLOR
        ================================================== */

        const colorButtons =
            document.querySelectorAll(
                ".color-option"
            );

        /* ==================================================
   THEME PRESET BUTTONS
================================================== */

const presetButtons =
    document.querySelectorAll(
        ".preset-option"
    );


function updatePresetButtons() {

    presetButtons.forEach(
        function (button) {

            const preset =
                button.dataset.preset;

            const presetData =
                presets[preset];

            button.classList.toggle(
                "active",
                presetData &&
                presetData.color === settings.color
            );

        }
    );

}


presetButtons.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                const presetName =
                    button.dataset.preset;

                const preset =
                    presets[presetName];


                if (!preset) {
                    return;
                }


                applyColor(
                    preset.color
                );


                settings.preset =
                    presetName;

                saveSettings();


                updatePresetButtons();

            }
        );

    }
);


        function updateColorButtons() {

            colorButtons.forEach(
                function (button) {

                    button.classList.toggle(
                        "active",
                        button.dataset.color ===
                            settings.color
                    );

                }
            );

        }


        function applyColor(colorName) {

            const color =
                colors[colorName];



            if (!color) {
                return;
            }


            document.documentElement.style.setProperty(
                "--primary",
                color.primary
            );


            document.documentElement.style.setProperty(
                "--primary-dark",
                color.dark
            );


            document.documentElement.style.setProperty(
                "--primary-light",
                color.primary + "15"
            );


            document.documentElement.style.setProperty(
                "--accent",
                color.primary
            );


            document.documentElement.style.setProperty(
                "--accent-color",
                color.primary
            );


            document.documentElement.style.setProperty(
                "--primary-color",
                color.primary
            );


            settings.color =
                colorName;
            
            settings.preset = null;

            saveSettings();

            updateColorButtons();

            updatePresetButtons();

        }


        colorButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        applyColor(
                            button.dataset.color
                        );

                    }
                );

            }
        );


        /* ==================================================
           THEME
        ================================================== */

        const themeButtons =
            document.querySelectorAll(
                ".theme-option"
            );


        function getSystemTheme() {

            return window.matchMedia(
                "(prefers-color-scheme: dark)"
            ).matches
                ? "dark"
                : "light";

        }


        function updateThemeButtons() {

            themeButtons.forEach(
                function (button) {

                    button.classList.toggle(
                        "active",
                        button.dataset.theme ===
                            settings.theme
                    );

                }
            );

        }


        function applyTheme(theme) {

            let actualTheme =
                theme;


            if (theme === "system") {

                actualTheme =
                    getSystemTheme();

            }


            document.documentElement.dataset.theme =
                actualTheme;


            document.documentElement.classList.toggle(
                "dark-theme",
                actualTheme === "dark"
            );


            settings.theme =
                theme;

            saveSettings();

            updateThemeButtons();

        }


        themeButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        applyTheme(
                            button.dataset.theme
                        );

                    }
                );

            }
        );


        /* ==================================================
           SIDEBAR
        ================================================== */

        const sidebarOptions =
            document.querySelectorAll(
                'input[name="sidebarMode"]'
            );


        function updateSidebarOptions() {

            sidebarOptions.forEach(
                function (input) {

                    input.checked =
                        input.value ===
                        settings.sidebar;

                }
            );

        }


        function applySidebar(mode) {

            const dashboardLayout =
                document.getElementById(
                    "dashboardLayout"
                );


            if (!dashboardLayout) {
                return;
            }


            if (mode === "compact") {

                dashboardLayout.classList.add(
                    "sidebar-collapsed"
                );

            } else {

                dashboardLayout.classList.remove(
                    "sidebar-collapsed"
                );

            }


            /*
             * Keep the existing sidebar preference
             * in sync with customization.
             */

            localStorage.setItem(
                "sidebarCollapsed",
                mode === "compact"
                    ? "true"
                    : "false"
            );


            settings.sidebar =
                mode;

            saveSettings();

            updateSidebarOptions();

        }


        sidebarOptions.forEach(
            function (input) {

                input.addEventListener(
                    "change",
                    function () {

                        applySidebar(
                            input.value
                        );

                    }
                );

            }
        );


        /* ==================================================
           DENSITY
        ================================================== */

        const densityOptions =
            document.querySelectorAll(
                'input[name="density"]'
            );


        function updateDensityOptions() {

            densityOptions.forEach(
                function (input) {

                    input.checked =
                        input.value ===
                        settings.density;

                }
            );

        }


        function applyDensity(density) {

            document.documentElement.classList.toggle(
                "compact-density",
                density === "compact"
            );


            settings.density =
                density;

            saveSettings();

            updateDensityOptions();

        }


        densityOptions.forEach(
            function (input) {

                input.addEventListener(
                    "change",
                    function () {

                        applyDensity(
                            input.value
                        );

                    }
                );

            }
        );


        /* ==================================================
           FONT
        ================================================== */

        const fontSelector =
            document.getElementById(
                "fontSelector"
            );


        function applyFont(font) {

            let fontFamily;


            if (font === "system") {

                fontFamily =
                    "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";

            } else {

                fontFamily =
                    "'" +
                    font +
                    "', sans-serif";

            }


            document.documentElement.style.setProperty(
                "--eventify-font",
                fontFamily
            );


            document.body.style.fontFamily =
                fontFamily;


            settings.font =
                font;

            saveSettings();


            if (fontSelector) {

                fontSelector.value =
                    font;

            }

        }


        if (fontSelector) {

            fontSelector.addEventListener(
                "change",
                function () {

                    applyFont(
                        fontSelector.value
                    );

                }
            );

        }


        /* ==================================================
           RESET
        ================================================== */

        if (resetButton) {

            resetButton.addEventListener(
                "click",
                function () {

                    settings = {
                        ...defaults
                    };


                    localStorage.removeItem(
                        "eventifyCustomization"
                    );


                    localStorage.setItem(
                        "sidebarCollapsed",
                        "false"
                    );


                    applyColor(
                        defaults.color
                    );


                    applyTheme(
                        defaults.theme
                    );


                    applySidebar(
                        defaults.sidebar
                    );


                    applyDensity(
                        defaults.density
                    );


                    applyFont(
                        defaults.font
                    );


                    closeCustomization();

                }
            );

        }


        /* ==================================================
           APPLY SAVED SETTINGS
        ================================================== */

        applyColor(
            settings.color
        );


        applyTheme(
            settings.theme
        );


        applySidebar(
            settings.sidebar
        );


        applyDensity(
            settings.density
        );


        applyFont(
            settings.font
        );


        updateColorButtons();

        updatePresetButtons();

        updateThemeButtons();

        updateThemeButtons();

        updateSidebarOptions();

        updateDensityOptions();

    }
);