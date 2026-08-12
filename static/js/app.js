document.addEventListener("DOMContentLoaded", function () {

    // Loader

    const loader = document.getElementById("page-loader");

    if(loader){

        window.addEventListener("load", ()=>{

            loader.classList.add("hide");

        });

    }

    // Back To Top

    const topBtn = document.getElementById("backToTop");

    if(topBtn){

        window.addEventListener("scroll", ()=>{

            if(window.scrollY>250){

                topBtn.classList.add("show");

            }else{

                topBtn.classList.remove("show");

            }

        });

        topBtn.addEventListener("click", ()=>{

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        });

    }

});

// Fullscreen

const fullscreenBtn=document.getElementById("fullscreenBtn");

if(fullscreenBtn){

    fullscreenBtn.addEventListener("click",()=>{

        if(!document.fullscreenElement){

            document.documentElement.requestFullscreen();

        }

        else{

            document.exitFullscreen();

        }

    });

}

/* ==========================================
   Animated Dashboard Counters
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    const counters = document.querySelectorAll(".stats-number");

    counters.forEach(counter => {

        let text = counter.innerText.trim();

        let prefix = "";

        let suffix = "";

        if (text.startsWith("₹")) {

            prefix = "₹";

            text = text.replace("₹", "");

        }

        if (text.includes("%")) {

            suffix = "%";

            text = text.replace("%", "");

        }

        const target = Number(text.replace(/,/g, ""));

        if (isNaN(target)) return;

        let current = 0;

        const duration = 1000;

        const increment = Math.max(target / 60, 1);

        function animate() {

            current += increment;

            if (current >= target) {

                counter.innerText = prefix + target.toLocaleString() + suffix;

                return;

            }

            counter.innerText =
                prefix +
                Math.floor(current).toLocaleString() +
                suffix;

            requestAnimationFrame(animate);

        }

        animate();

    });

});