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

document.addEventListener("DOMContentLoaded", function () {

    const panel = document.getElementById("customizationPanel");
    const overlay = document.getElementById("customizationOverlay");
    const openButton = document.getElementById("customizeToggle");
    const closeButton = document.getElementById("customizationClose");
    const resetButton = document.getElementById("resetCustomization");

    if (!panel || !overlay || !openButton) {
        return;
    }


    /* ======================================================
       DEFAULT SETTINGS
    ====================================================== */

    const defaults = {
        theme: "light",
        preset: "default",
        color: "indigo",
        sidebar: "expanded",
        density: "comfortable",
        font: "Poppins"
    };


    /* ======================================================
       ACCENT COLORS
    ====================================================== */

    const colors = {

        indigo: {
            primary: "#4f46e5",
            dark: "#4338ca",
            light: "#eef2ff"
        },

        blue: {
            primary: "#2563eb",
            dark: "#1d4ed8",
            light: "#eff6ff"
        },

        purple: {
            primary: "#7c3aed",
            dark: "#6d28d9",
            light: "#f5f3ff"
        },

        green: {
            primary: "#16a34a",
            dark: "#15803d",
            light: "#f0fdf4"
        },

        orange: {
            primary: "#ea580c",
            dark: "#c2410c",
            light: "#fff7ed"
        },

        red: {
            primary: "#dc2626",
            dark: "#b91c1c",
            light: "#fef2f2"
        },

        pink: {
            primary: "#db2777",
            dark: "#be185d",
            light: "#fdf2f8"
        }

    };


    /* ======================================================
       THEME PRESETS
    ====================================================== */

    const presets = {

    default: {
        color: "indigo",
        primary: "#4f46e5",
        primaryDark: "#4338ca",
        primaryLight: "#eef2ff",
        gradientStart: "#4f46e5",
        gradientEnd: "#6366f1"
    },

    ocean: {
        color: "blue",
        primary: "#2563eb",
        primaryDark: "#1d4ed8",
        primaryLight: "#eff6ff",
        gradientStart: "#0891b2",
        gradientEnd: "#2563eb"
    },

    emerald: {
        color: "green",
        primary: "#16a34a",
        primaryDark: "#15803d",
        primaryLight: "#f0fdf4",
        gradientStart: "#059669",
        gradientEnd: "#16a34a"
    },

    sunset: {
        color: "orange",
        primary: "#ea580c",
        primaryDark: "#c2410c",
        primaryLight: "#fff7ed",
        gradientStart: "#f97316",
        gradientEnd: "#dc2626"
    },

    rose: {
        color: "pink",
        primary: "#db2777",
        primaryDark: "#be185d",
        primaryLight: "#fdf2f8",
        gradientStart: "#e11d48",
        gradientEnd: "#db2777"
    }

};


    /* ======================================================
       LOAD SETTINGS
    ====================================================== */

    let settings = {
        ...defaults
    };

    try {

        const saved =
            localStorage.getItem("eventifyCustomization");

        if (saved) {

            settings = {
                ...defaults,
                ...JSON.parse(saved)
            };

        }

    } catch (error) {

        console.warn(
            "Unable to load Eventify customization settings.",
            error
        );

    }


    /* ======================================================
       SAVE SETTINGS
    ====================================================== */

    function saveSettings() {

        localStorage.setItem(
            "eventifyCustomization",
            JSON.stringify(settings)
        );

    }


    /* ======================================================
       OPEN / CLOSE PANEL
    ====================================================== */

    function openCustomization() {

        panel.classList.add("active");
        overlay.classList.add("active");

        document.body.style.overflow = "hidden";

    }


    function closeCustomization() {

        panel.classList.remove("active");
        overlay.classList.remove("active");

        document.body.style.overflow = "";

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


    /* ======================================================
       COLOR BUTTONS
    ====================================================== */

    const colorButtons =
        document.querySelectorAll(".color-option");


    function updateColorButtons() {

        colorButtons.forEach(function (button) {

            button.classList.toggle(
                "active",
                button.dataset.color === settings.color
            );

        });

    }


    /* ======================================================
       APPLY ACCENT COLOR
    ====================================================== */

    function applyColor(colorName, shouldSave = true) {

    const color = colors[colorName];

    if (!color) {
        return;
    }

    const root = document.documentElement;

    /* ==========================================
       PRIMARY COLORS
    ========================================== */

    root.style.setProperty(
        "--primary",
        color.primary
    );

    root.style.setProperty(
        "--primary-dark",
        color.dark
    );

    root.style.setProperty(
        "--primary-hover",
        color.dark
    );

    root.style.setProperty(
        "--primary-light",
        color.light
    );

    root.style.setProperty(
        "--accent",
        color.primary
    );

    root.style.setProperty(
        "--accent-color",
        color.primary
    );

    root.style.setProperty(
        "--primary-color",
        color.primary
    );


    /* ==========================================
       THEME GRADIENT
    ========================================== */

    root.style.setProperty(
        "--theme-gradient-start",
        color.primary
    );

    root.style.setProperty(
        "--theme-gradient-end",
        color.dark
    );


    /* ==========================================
       EXTRA THEME VARIABLES
    ========================================== */

    root.style.setProperty(
        "--theme-shadow",
        `rgba(
            ${parseInt(color.primary.slice(1, 3), 16)},
            ${parseInt(color.primary.slice(3, 5), 16)},
            ${parseInt(color.primary.slice(5, 7), 16)},
            .25
        )`
    );


    settings.color = colorName;

    if (shouldSave) {
        saveSettings();
    }

    updateColorButtons();

}


    colorButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                settings.preset = null;

                applyColor(
                    button.dataset.color
                );

                updatePresetButtons();

                saveSettings();

            }
        );

    });


    /* ======================================================
       PRESET BUTTONS
    ====================================================== */

    const presetButtons =
        document.querySelectorAll(".preset-option");


    function updatePresetButtons() {

        presetButtons.forEach(function (button) {

            const presetName =
                button.dataset.preset;

            button.classList.toggle(
                "active",
                settings.preset === presetName
            );

        });

    }


    presetButtons.forEach(function (button) {

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


                settings.preset =
                    presetName;


                applyColor(
                    preset.color,
                    false
                );


                saveSettings();

                updatePresetButtons();

            }
        );

    });


    /* ======================================================
       THEME
    ====================================================== */

    const themeButtons =
        document.querySelectorAll(".theme-option");


    function getSystemTheme() {

        return window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches
            ? "dark"
            : "light";

    }


    function getActualTheme(theme) {

        if (theme === "system") {
            return getSystemTheme();
        }

        return theme;

    }


    function applyTheme(theme, shouldSave = true) {

        const actualTheme =
            getActualTheme(theme);


        const root =
            document.documentElement;


        root.dataset.theme =
            actualTheme;


        root.classList.toggle(
            "dark-theme",
            actualTheme === "dark"
        );


        root.classList.toggle(
            "light-theme",
            actualTheme === "light"
        );


        settings.theme =
            theme;


        if (shouldSave) {
            saveSettings();
        }


        updateThemeButtons();

    }


    function updateThemeButtons() {

        themeButtons.forEach(function (button) {

            button.classList.toggle(
                "active",
                button.dataset.theme === settings.theme
            );

        });

    }


    themeButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                applyTheme(
                    button.dataset.theme
                );

            }
        );

    });


    /* ======================================================
       SYSTEM THEME LISTENER
    ====================================================== */

    const systemThemeQuery =
        window.matchMedia(
            "(prefers-color-scheme: dark)"
        );


    systemThemeQuery.addEventListener(
        "change",
        function () {

            if (settings.theme === "system") {

                applyTheme(
                    "system",
                    false
                );

            }

        }
    );


    /* ======================================================
       SIDEBAR
    ====================================================== */

    const sidebarOptions =
        document.querySelectorAll(
            'input[name="sidebarMode"]'
        );


    function updateSidebarOptions() {

        sidebarOptions.forEach(function (input) {

            input.checked =
                input.value === settings.sidebar;

        });

    }


    function applySidebar(mode, shouldSave = true) {

        const dashboardLayout =
            document.getElementById(
                "dashboardLayout"
            );

        if (!dashboardLayout) {
            return;
        }


        dashboardLayout.classList.toggle(
            "sidebar-collapsed",
            mode === "compact"
        );


        localStorage.setItem(
            "sidebarCollapsed",
            mode === "compact"
                ? "true"
                : "false"
        );


        settings.sidebar =
            mode;


        if (shouldSave) {
            saveSettings();
        }


        updateSidebarOptions();

    }


    sidebarOptions.forEach(function (input) {

        input.addEventListener(
            "change",
            function () {

                applySidebar(
                    input.value
                );

            }
        );

    });


    /* ======================================================
       DENSITY
    ====================================================== */

    const densityOptions =
        document.querySelectorAll(
            'input[name="density"]'
        );


    function updateDensityOptions() {

        densityOptions.forEach(function (input) {

            input.checked =
                input.value === settings.density;

        });

    }


    function applyDensity(
        density,
        shouldSave = true
    ) {

        document.documentElement.classList.toggle(
            "compact-density",
            density === "compact"
        );


        settings.density =
            density;


        if (shouldSave) {
            saveSettings();
        }


        updateDensityOptions();

    }


    densityOptions.forEach(function (input) {

        input.addEventListener(
            "change",
            function () {

                applyDensity(
                    input.value
                );

            }
        );

    });


    /* ======================================================
       FONT
    ====================================================== */

    const fontSelector =
        document.getElementById(
            "fontSelector"
        );


    function applyFont(
        font,
        shouldSave = true
    ) {

        let fontFamily;


        if (font === "system") {

            fontFamily =
                "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";

        } else {

            fontFamily =
                "'" + font + "', sans-serif";

        }


        document.documentElement.style.setProperty(
            "--eventify-font",
            fontFamily
        );


        document.body.style.fontFamily =
            fontFamily;


        settings.font =
            font;


        if (fontSelector) {

            fontSelector.value =
                font;

        }


        if (shouldSave) {
            saveSettings();
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


    /* ======================================================
       RESET
    ====================================================== */

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


                /* Remove inline theme variables */

                const root =
                    document.documentElement;

                [
                    "--primary",
                    "--primary-dark",
                    "--primary-hover",
                    "--primary-light",
                    "--accent",
                    "--accent-color",
                    "--primary-color",
                    "--eventify-font"
                ].forEach(function (variable) {

                    root.style.removeProperty(
                        variable
                    );

                });


                root.classList.remove(
                    "dark-theme",
                    "light-theme",
                    "compact-density"
                );


                applyColor(
                    defaults.color,
                    false
                );


                applyTheme(
                    defaults.theme,
                    false
                );


                applySidebar(
                    defaults.sidebar,
                    false
                );


                applyDensity(
                    defaults.density,
                    false
                );


                applyFont(
                    defaults.font,
                    false
                );


                saveSettings();

                updatePresetButtons();

                closeCustomization();

            }
        );

    }


    /* ======================================================
       APPLY SAVED SETTINGS
    ====================================================== */

    applyColor(
        settings.color,
        false
    );


    applyTheme(
        settings.theme,
        false
    );


    applySidebar(
        settings.sidebar,
        false
    );


    applyDensity(
        settings.density,
        false
    );


    applyFont(
        settings.font,
        false
    );


    updateColorButtons();
    updatePresetButtons();
    updateThemeButtons();
    updateSidebarOptions();
    updateDensityOptions();

});