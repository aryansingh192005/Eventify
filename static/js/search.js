document.addEventListener("DOMContentLoaded",()=>{

const searchInput=document.getElementById("globalSearch");

const searchResults=document.getElementById("searchResults");

if(!searchInput) return;

const pages=[

{
title:"Dashboard",
icon:"bi-speedometer2",
url:"/dashboard/",
desc:"Dashboard overview"
},

{
title:"Events",
icon:"bi-calendar-event",
url:"/events/",
desc:"Browse all events"
},

{
title:"Calendar",
icon:"bi-calendar3",
url:"/calendar/",
desc:"Monthly calendar"
},

{
title:"Reports",
icon:"bi-bar-chart",
url:"/reports/",
desc:"Analytics & reports"
},

{
title:"Profile",
icon:"bi-person-circle",
url:"/profile/",
desc:"Manage profile"
},

{
title:"Notifications",
icon:"bi-bell",
url:"/notifications/",
desc:"Latest notifications"
}

];

searchInput.addEventListener("input",()=>{

const value=searchInput.value.toLowerCase().trim();

searchResults.innerHTML="";

if(value===""){

searchResults.classList.remove("show");

return;

}

const filtered=pages.filter(p=>

p.title.toLowerCase().includes(value) ||

p.desc.toLowerCase().includes(value)

);

filtered.forEach(item=>{

const div=document.createElement("div");

div.className="search-item";

div.innerHTML=`

<i class="bi ${item.icon}"></i>

<div>

<h6>${item.title}</h6>

<small>${item.desc}</small>

</div>

`;

div.onclick=()=>{

window.location=item.url;

};

searchResults.appendChild(div);

});

searchResults.classList.toggle("show",filtered.length>0);

});

document.addEventListener("click",(e)=>{

if(!e.target.closest(".search-wrapper")){

searchResults.classList.remove("show");

}

});

});