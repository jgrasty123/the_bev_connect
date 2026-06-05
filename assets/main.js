const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav');
if (burger) burger.addEventListener('click', () => nav.classList.toggle('open'));
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el, i) => {
  el.style.transitionDelay = (i % 4 * 60) + 'ms';
  io.observe(el);
});
