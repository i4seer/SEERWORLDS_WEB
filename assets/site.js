
const menuBtn=document.querySelector(".menu-btn");
const nav=document.querySelector(".main-nav");
if(menuBtn&&nav){
  menuBtn.addEventListener("click",()=>{
    const open=nav.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded",String(open));
  });
  nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>nav.classList.remove("open")));
}
