/* Nav scroll */
const nav=document.querySelector('.nav');
window.addEventListener('scroll',()=>{nav.style.padding=window.scrollY>20?'9px 20px':'';},{passive:true});

/* Billing toggle */
let annual=true;
const prices={proA:7,proM:9,teamA:22,teamM:29};
function toggleBilling(){
  annual=!annual;
  document.getElementById('billing-toggle').classList.toggle('monthly',!annual);
  document.getElementById('pro-price').textContent=annual?prices.proA:prices.proM;
  document.getElementById('team-price').textContent=annual?prices.teamA:prices.teamM;
  document.getElementById('pro-note').textContent=annual?`Billed $${prices.proA*12}/year · save $${(prices.proM-prices.proA)*12}`:'Billed monthly';
  document.getElementById('team-note').textContent=annual?`Billed $${prices.teamA*12}/year · save $${(prices.teamM-prices.teamA)*12}`:'Billed monthly';
}

/* FAQ */
function toggleFaq(el){
  const open=el.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i=>i.classList.remove('open'));
  if(!open)el.classList.add('open');
}

/* Scroll reveal */
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')});
},{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));