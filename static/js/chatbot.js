/* ==========================================================
   EVENTIFY CHATBOT
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const chatbot = document.getElementById(
        "eventifyChatbot"
    );

    const toggle = document.getElementById(
        "chatbotToggle"
    );

    const closeButton = document.getElementById(
        "chatbotClose"
    );

    const windowElement = document.getElementById(
        "chatbotWindow"
    );

    const form = document.getElementById(
        "chatbotForm"
    );

    const input = document.getElementById(
        "chatbotInput"
    );

    const messages = document.getElementById(
        "chatbotMessages"
    );

    const typing = document.getElementById(
        "chatbotTyping"
    );


    /* ======================================================
       SAFETY CHECK
    ====================================================== */

    if (
        !chatbot ||
        !toggle ||
        !closeButton ||
        !windowElement ||
        !form ||
        !input ||
        !messages
    ) {

        console.error(
            "Eventify chatbot elements were not found."
        );

        return;

    }


    /* ======================================================
       OPEN CHAT
    ====================================================== */

    toggle.addEventListener(
        "click",
        function () {

            windowElement.classList.toggle(
                "active"
            );


            if (
                windowElement.classList.contains(
                    "active"
                )
            ) {

                input.focus();

            }

        }
    );


    /* ======================================================
       CLOSE CHAT
    ====================================================== */

    closeButton.addEventListener(
        "click",
        function () {

            windowElement.classList.remove(
                "active"
            );

        }
    );


    /* ======================================================
       CLOSE WITH ESC
    ====================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape"
            ) {

                windowElement.classList.remove(
                    "active"
                );

            }

        }
    );


    /* ======================================================
       CSRF TOKEN
    ====================================================== */

    function getCookie(name) {

        const cookies =
            document.cookie.split(";");


        for (
            let cookie of cookies
        ) {

            cookie = cookie.trim();


            if (
                cookie.startsWith(
                    name + "="
                )
            ) {

                return decodeURIComponent(
                    cookie.substring(
                        name.length + 1
                    )
                );

            }

        }


        return null;

    }


    /* ======================================================
       ADD MESSAGE
    ====================================================== */

    function addMessage(
        text,
        sender,
        links = []
    ) {

        const wrapper =
            document.createElement(
                "div"
            );


        wrapper.className =
            `chatbot-message ${sender}`;


        const content =
            document.createElement(
                "div"
            );


        content.className =
            "chatbot-bubble";


        const textElement =
            document.createElement(
                "div"
            );


        textElement.textContent =
            text;


        content.appendChild(
            textElement
        );


        /* ==================================================
           NAVIGATION / ACTION LINKS
        ================================================== */

        if (
            Array.isArray(links) &&
            links.length > 0
        ) {

            const linksContainer =
                document.createElement(
                    "div"
                );


            linksContainer.className =
                "chatbot-links";


            links.forEach(
                function (link) {

                    if (
                        !link.label ||
                        !link.url
                    ) {

                        return;

                    }


                    const anchor =
                        document.createElement(
                            "a"
                        );


                    anchor.href =
                        link.url;


                    anchor.className =
                        "chatbot-link";


                    anchor.textContent =
                        link.label;


                    /* ========================================
                       CONFIRM CANCELLATION
                    ======================================== */

                    if (
                        link.action ===
                        "confirm_cancel"
                    ) {

                        anchor.href = "#";


                        anchor.addEventListener(
                            "click",
                            function (event) {

                                event.preventDefault();

                                event.stopPropagation();


                                confirmCancellation(
                                    link.registration_id,
                                    link.event_title
                                );

                            }
                        );

                    }


                    /* ========================================
                       CANCEL CONFIRMATION
                    ======================================== */

                    else if (
                        link.action ===
                        "cancel_confirmation"
                    ) {

                        anchor.href = "#";


                        anchor.addEventListener(
                            "click",
                            function (event) {

                                event.preventDefault();

                                event.stopPropagation();


                                addMessage(
                                    "Okay, I’ll keep your registration. 👍",
                                    "bot"
                                );

                            }
                        );

                    }


                    /* ========================================
                       NORMAL NAVIGATION LINK
                    ======================================== */

                    else {

                        anchor.target =
                            "_self";

                    }


                    /* ========================================
                       LINK ICON
                    ======================================== */

                    const icon =
                        document.createElement(
                            "i"
                        );


                    icon.className =
                        "bi bi-arrow-right";


                    anchor.appendChild(
                        icon
                    );


                    linksContainer.appendChild(
                        anchor
                    );

                }
            );


            content.appendChild(
                linksContainer
            );

        }


        wrapper.appendChild(
            content
        );


        messages.appendChild(
            wrapper
        );


        messages.scrollTop =
            messages.scrollHeight;

    }


    /* ======================================================
       TYPING INDICATOR
    ====================================================== */

    function showTyping() {

        if (!typing) {

            return;

        }


        typing.classList.add(
            "active"
        );


        messages.scrollTop =
            messages.scrollHeight;

    }


    function hideTyping() {

        if (!typing) {

            return;

        }


        typing.classList.remove(
            "active"
        );

    }


    /* ======================================================
       CONFIRM CANCELLATION
       
       IMPORTANT:
       This function is INSIDE DOMContentLoaded so it can
       access addMessage().
    ====================================================== */

    async function confirmCancellation(
        registrationId,
        eventTitle
    ) {

        console.log(
            "Cancellation clicked:",
            registrationId,
            eventTitle
        );


        addMessage(
            `Cancelling your ${eventTitle} registration...`,
            "bot"
        );


        try {

            const response =
                await fetch(
                    `/my-registrations/${registrationId}/cancel/`,
                    {
                        method: "GET",

                        credentials:
                            "same-origin",

                        headers: {
                            "X-Requested-With":
                                "XMLHttpRequest"
                        }
                    }
                );


            console.log(
                "Cancellation response:",
                response.status,
                response.url
            );


            /* ==============================================
               SUCCESS
            ============================================== */

            if (
                response.ok ||
                response.redirected
            ) {

                addMessage(
                    `Your registration for ${eventTitle} `
                    + `has been cancelled successfully. ✅`,
                    "bot"
                );


                addMessage(
                    "Your registration list has been updated.",
                    "bot",
                    [
                        {
                            label:
                                "My Registrations",

                            url:
                                "/my-registrations/"
                        }
                    ]
                );


                return;

            }


            /* ==============================================
               SERVER ERROR
            ============================================== */

            addMessage(
                "I couldn't cancel the registration. Please try again.",
                "bot"
            );

        }

        catch (error) {

            console.error(
                "Cancellation error:",
                error
            );


            addMessage(
                "Something went wrong while cancelling your registration.",
                "bot"
            );

        }

    }


    /* ======================================================
       SEND MESSAGE
    ====================================================== */

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const message =
                input.value.trim();


            if (!message) {

                return;

            }


            /* ----------------------------------------------
               USER MESSAGE
            ---------------------------------------------- */

            addMessage(
                message,
                "user"
            );


            input.value = "";

            input.disabled = true;


            const sendButton =
                form.querySelector(
                    "button"
                );


            if (sendButton) {

                sendButton.disabled =
                    true;

            }


            showTyping();


            try {

                const csrfToken =
                    getCookie(
                        "csrftoken"
                    );


                const formData =
                    new URLSearchParams();


                formData.append(
                    "message",
                    message
                );


                const response =
                    await fetch(
                        "/chatbot/api/chat/",
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/x-www-form-urlencoded",

                                "X-CSRFToken":
                                    csrfToken,

                            },

                            body:
                                formData.toString(),

                        }
                    );


                const data =
                    await response.json();


                hideTyping();


                if (
                    data.reply
                ) {

                    addMessage(
                        data.reply,
                        "bot",
                        data.links || []
                    );

                }

                else {

                    addMessage(
                        "Sorry, something went wrong.",
                        "bot"
                    );

                }

            }

            catch (error) {

                console.error(
                    "Chatbot error:",
                    error
                );


                hideTyping();


                addMessage(
                    "I couldn't connect to the Eventify server. Please try again.",
                    "bot"
                );

            }


            input.disabled = false;


            if (sendButton) {

                sendButton.disabled =
                    false;

            }


            input.focus();

        }
    );

});