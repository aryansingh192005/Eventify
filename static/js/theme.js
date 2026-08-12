const html=document.documentElement;

const savedTheme=localStorage.getItem("theme");

if(savedTheme){

    html.setAttribute("data-theme",savedTheme);

}

function toggleTheme(){

    const current=html.getAttribute("data-theme");

    if(current==="dark"){

        html.removeAttribute("data-theme");

        localStorage.setItem("theme","light");

    }

    else{

        html.setAttribute("data-theme","dark");

        localStorage.setItem("theme","dark");

    }

    updateThemeIcon();

}

function updateThemeIcon(){

    const icon=document.getElementById("themeIcon");

    if(!icon) return;

    if(html.getAttribute("data-theme")==="dark"){

        icon.className="bi bi-sun-fill";

    }

    else{

        icon.className="bi bi-moon-stars-fill";

    }

}

document.addEventListener("DOMContentLoaded",updateThemeIcon);