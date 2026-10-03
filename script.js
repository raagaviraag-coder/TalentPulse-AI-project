// ===========================
// TalentPulse AI Animations
// ===========================

// Page Fade-in
window.addEventListener("load", () => {
    document.body.style.opacity = "1";
});

// Mouse Glow Effect
document.addEventListener("mousemove", (e) => {

    const glow = document.querySelector(".mouse-glow");

    if(glow){

        glow.style.left = e.clientX + "px";
        glow.style.top = e.clientY + "px";

    }

});

// Create Mouse Glow
const glow = document.createElement("div");

glow.className = "mouse-glow";

document.body.appendChild(glow);


// Smooth Card Hover
const cards = document.querySelectorAll(".glass-card");

cards.forEach(card=>{

    card.addEventListener("mousemove",(e)=>{

        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        card.style.background =
        `radial-gradient(circle at ${x}px ${y}px,
        rgba(255,255,255,.20),
        rgba(255,255,255,.08))`;

    });

    card.addEventListener("mouseleave",()=>{

        card.style.background="rgba(255,255,255,.08)";

    });

});


// Animated Progress Bar
window.addEventListener("load",()=>{

const bar=document.querySelector(".progress-fill");

if(bar){

const width=bar.style.width;

bar.style.width="0%";

setTimeout(()=>{

bar.style.width=width;

},400);

}

});


// Number Count Animation
const counters=document.querySelectorAll(".counter");

counters.forEach(counter=>{

const update=()=>{

const target=+counter.getAttribute("data-target");

const current=+counter.innerText;

const increment=target/80;

if(current<target){

counter.innerText=Math.ceil(current+increment);

setTimeout(update,20);

}

else{

counter.innerText=target;

}

}

update();

});


// Button Ripple Effect

const btn=document.querySelector(".predict-btn");

if(btn){

btn.addEventListener("click",function(e){

let ripple=document.createElement("span");

ripple.classList.add("ripple");

this.appendChild(ripple);

let x=e.clientX-this.offsetLeft;
let y=e.clientY-this.offsetTop;

ripple.style.left=x+"px";
ripple.style.top=y+"px";

setTimeout(()=>{

ripple.remove();

},700);

});

}


// Floating Title Animation

const title=document.querySelector(".logo h1");

let angle=0;

setInterval(()=>{

angle+=0.02;

title.style.transform=`translateY(${Math.sin(angle)*4}px)`;

},20);


// Random Glow Effect

setInterval(()=>{

document.querySelectorAll(".glass-card").forEach(card=>{

card.style.boxShadow=
`0 20px 50px rgba(${Math.random()*100},
${Math.random()*180},
255,.35)`;

});

},3000);