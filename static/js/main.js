/* SignLang AI — main.js: global effects */
"use strict";

// ── Custom cursor ────────────────────────────────────────────
const dot  = document.getElementById("cursorDot");
const ring = document.getElementById("cursorRing");
if (dot && ring) {
  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener("mousemove", e => { mx = e.clientX; my = e.clientY; });
  const lerp = (a,b,t) => a + (b-a)*t;
  function animCursor() {
    rx = lerp(rx, mx, 0.14);
    ry = lerp(ry, my, 0.14);
    dot.style.transform  = `translate(${mx-3}px,${my-3}px)`;
    ring.style.transform = `translate(${rx-16}px,${ry-16}px)`;
    requestAnimationFrame(animCursor);
  }
  animCursor();

  document.querySelectorAll("a,button,.feat-card,.dict-item,.qa-btn,.step-orb").forEach(el => {
    el.addEventListener("mouseenter", () => ring.classList.add("hover"));
    el.addEventListener("mouseleave", () => ring.classList.remove("hover"));
  });
}

// ── Navbar scroll ────────────────────────────────────────────
const nav = document.getElementById("navbar");
if (nav) {
  window.addEventListener("scroll", () => {
    nav.classList.toggle("scrolled", window.scrollY > 24);
  }, { passive: true });
}

// ── Scroll reveal ────────────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = "1";
      e.target.style.transform = "translateY(0)";
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".feat-card, .step, .h-stat").forEach((el, i) => {
  el.style.opacity    = "0";
  el.style.transform  = "translateY(28px)";
  el.style.transition = `opacity 0.55s ease ${i * 0.07}s, transform 0.55s ease ${i * 0.07}s`;
  observer.observe(el);
});

// ── Hero number counter animation ────────────────────────────
function animCount(el, target, suffix, duration = 1800) {
  let start = null;
  const step = ts => {
    if (!start) start = ts;
    const p   = Math.min((ts - start) / duration, 1);
    const val = Math.floor(p * target);
    el.textContent = val + suffix;
    if (p < 1) requestAnimationFrame(step);
    else el.textContent = target + suffix;
  };
  requestAnimationFrame(step);
}

const statsObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target;
    const raw = el.dataset.count;
    if (!raw) return;
    const [num, suf] = raw.split("|");
    animCount(el, parseFloat(num), suf || "");
    statsObs.unobserve(el);
  });
}, { threshold: 0.5 });

document.querySelectorAll("[data-count]").forEach(el => statsObs.observe(el));