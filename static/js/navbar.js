document.addEventListener("DOMContentLoaded",function(){

    const navbar=document.querySelector(".navbar");

    function updateNavbar(){

        if(window.scrollY>20){

            navbar.classList.add("scrolled");

        }

        else{

            navbar.classList.remove("scrolled");

        }

    }

    updateNavbar();

    window.addEventListener("scroll",updateNavbar);

});