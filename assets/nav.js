document.addEventListener('DOMContentLoaded',()=>{
  const toggle=document.querySelector('.menu-toggle');
  if(!toggle) return;
  const nav=toggle.parentNode.querySelector('nav');
  toggle.addEventListener('click',()=>{
    nav.parentNode.classList.toggle('open');
  });
  nav.querySelectorAll('a').forEach(link=>{
    link.addEventListener('click',()=>{
      nav.parentNode.classList.remove('open');
    });
  });
});
