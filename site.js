/* ==========================================================================
   AKINTAYO — interaction layer
   Principles: the page is complete and readable before this file runs.
   Everything here is enhancement, gated on motion preference and pointer type.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var motion = !reduced.matches;

  /* Only now do we allow elements to start hidden. Without JS, or with
     reduced motion, the page renders finished. */
  if (motion) root.classList.add("anim");

  var rafPending = false;
  var scrollCbs = [];
  function onScroll(fn) { scrollCbs.push(fn); }
  function fireScroll() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(function () {
      rafPending = false;
      for (var i = 0; i < scrollCbs.length; i++) scrollCbs[i]();
    });
  }
  window.addEventListener("scroll", fireScroll, { passive: true });
  window.addEventListener("resize", fireScroll, { passive: true });

  /* ------------------------------------------------------------- 1. Nav */
  var nav = document.querySelector(".nav");
  var lastY = window.scrollY;
  if (nav) {
    onScroll(function () {
      var y = window.scrollY;
      nav.classList.toggle("is-stuck", y > 24);
      if (!document.body.classList.contains("menu-open")) {
        nav.classList.toggle("is-hidden", y > 420 && y > lastY + 4);
      }
      lastY = y;
    });
  }

  var burger = document.querySelector(".burger");
  var menu = document.querySelector(".menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      menu.setAttribute("aria-hidden", open ? "false" : "true");
      document.body.style.overflow = open ? "hidden" : "";
      if (open && nav) nav.classList.remove("is-hidden");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        document.body.classList.remove("menu-open");
        document.body.style.overflow = "";
        burger.setAttribute("aria-expanded", "false");
      }
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("menu-open")) burger.click();
    });
  }

  /* -------------------------------------------------- 2. Scroll progress */
  var bar = document.querySelector(".progress");
  if (bar) {
    onScroll(function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? Math.min(1, window.scrollY / h) : 0;
      bar.style.transform = "scaleX(" + p + ")";
    });
  }

  /* ----------------------------------------------------- 3. Reveal layer */
  var revealTargets = document.querySelectorAll("[data-reveal], .lines, .arc, .bars");

  function showAll() {
    for (var i = 0; i < revealTargets.length; i++) revealTargets[i].classList.add("is-in");
  }

  if (!motion || !("IntersectionObserver" in window)) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var delay = el.getAttribute("data-delay");
        if (delay) el.style.setProperty("--d", delay + "ms");
        el.classList.add("is-in");
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -9% 0px", threshold: 0.08 });

    for (var r = 0; r < revealTargets.length; r++) io.observe(revealTargets[r]);

    /* Stagger siblings inside a group without hand-written delays */
    var groups = document.querySelectorAll("[data-stagger]");
    for (var g = 0; g < groups.length; g++) {
      var kids = groups[g].querySelectorAll(":scope > [data-reveal]");
      for (var k = 0; k < kids.length; k++) kids[k].style.setProperty("--d", (k * 80) + "ms");
    }

    /* Failsafe: nothing stays invisible, whatever happens. */
    setTimeout(showAll, 3600);
  }

  /* Hero content animates on load rather than on scroll, so the first frame
     resolves immediately. */
  requestAnimationFrame(function () {
    var above = document.querySelectorAll("[data-onload]");
    for (var i = 0; i < above.length; i++) above[i].classList.add("is-in");
  });

  /* -------------------------------------------------------- 4. Parallax */
  var pars = Array.prototype.slice.call(document.querySelectorAll("[data-par]"));
  if (motion && pars.length) {
    onScroll(function () {
      var vh = window.innerHeight;
      for (var i = 0; i < pars.length; i++) {
        var el = pars[i];
        var box = el.getBoundingClientRect();
        if (box.bottom < -200 || box.top > vh + 200) continue;
        var amt = parseFloat(el.getAttribute("data-par")) || 8;
        var mid = box.top + box.height / 2;
        var off = ((mid - vh / 2) / vh) * -amt;
        el.style.transform = "translate3d(0," + off.toFixed(2) + "%,0) scale(1.1)";
      }
    });
    fireScroll();
  }

  /* -------------------------------------------------------- 5. Cursor */
  var cursor = document.querySelector(".cursor");
  var dot = document.querySelector(".cursor-dot");
  if (cursor && dot && fine.matches && motion) {
    document.body.classList.add("has-cursor");
    var cx = window.innerWidth / 2, cy = window.innerHeight / 2;
    var tx = cx, ty = cy, dx = cx, dy = cy;
    var label = cursor.querySelector(".cursor__label");

    window.addEventListener("mousemove", function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!cursor.classList.contains("is-ready")) {
        cursor.classList.add("is-ready"); dot.classList.add("is-ready");
        cx = tx; cy = ty; dx = tx; dy = ty;
      }
    }, { passive: true });

    document.addEventListener("mouseleave", function () {
      cursor.classList.add("is-hidden"); dot.classList.add("is-hidden");
    });
    document.addEventListener("mouseenter", function () {
      cursor.classList.remove("is-hidden"); dot.classList.remove("is-hidden");
    });

    (function loop() {
      cx += (tx - cx) * 0.16;
      cy += (ty - cy) * 0.16;
      dx += (tx - dx) * 0.62;
      dy += (ty - dy) * 0.62;
      cursor.style.transform = "translate3d(" + cx + "px," + cy + "px,0)";
      dot.style.transform = "translate3d(" + dx + "px," + dy + "px,0)";
      requestAnimationFrame(loop);
    })();

    document.addEventListener("mouseover", function (e) {
      var view = e.target.closest("[data-cursor]");
      if (view) {
        cursor.classList.add("is-view");
        cursor.classList.remove("is-link");
        if (label) label.textContent = view.getAttribute("data-cursor");
        return;
      }
      if (e.target.closest("a, button, input, textarea, summary")) {
        cursor.classList.add("is-link");
        cursor.classList.remove("is-view");
      }
    });
    document.addEventListener("mouseout", function (e) {
      if (e.target.closest("[data-cursor]") || e.target.closest("a, button, input, textarea, summary")) {
        var to = e.relatedTarget;
        if (to && (to.closest("[data-cursor]") || to.closest("a, button"))) return;
        cursor.classList.remove("is-link", "is-view");
      }
    });
  }

  /* ------------------------------------------------------ 6. Magnetic */
  if (fine.matches && motion) {
    var mags = document.querySelectorAll("[data-magnet]");
    Array.prototype.forEach.call(mags, function (el) {
      var strength = parseFloat(el.getAttribute("data-magnet")) || 0.28;
      el.addEventListener("mousemove", function (e) {
        var b = el.getBoundingClientRect();
        var mx = e.clientX - (b.left + b.width / 2);
        var my = e.clientY - (b.top + b.height / 2);
        el.style.transform = "translate(" + (mx * strength) + "px," + (my * strength) + "px)";
      });
      el.addEventListener("mouseleave", function () {
        el.style.transition = "transform .55s cubic-bezier(.22,1,.36,1)";
        el.style.transform = "translate(0,0)";
        setTimeout(function () { el.style.transition = ""; }, 560);
      });
    });
  }

  /* ----------------------------------- 7. Cursor-following work preview */
  var peek = document.querySelector(".peek");
  var rows = document.querySelectorAll("[data-peek-stat]");
  if (peek && rows.length && fine.matches && motion) {
    var items = {};
    Array.prototype.forEach.call(rows, function (row, i) {
      var item = document.createElement("div");
      item.className = "peek__item";
      var stat = document.createElement("p");
      stat.className = "peek__stat";
      stat.textContent = row.getAttribute("data-peek-stat") || "";
      var sub = document.createElement("p");
      sub.className = "peek__sub";
      sub.textContent = row.getAttribute("data-peek-sub") || "";
      item.appendChild(stat);
      item.appendChild(sub);
      peek.appendChild(item);
      items[i] = item;
      row.setAttribute("data-peek-i", String(i));
    });

    var px = 0, py = 0, cxp = 0, cyp = 0, scale = 0.86, peeking = false;
    peek.style.transition = "opacity .4s cubic-bezier(.22,1,.36,1)";

    document.addEventListener("mousemove", function (e) { px = e.clientX; py = e.clientY; }, { passive: true });

    (function peekLoop() {
      var ease = peeking ? 0.12 : 0.3;
      cxp += (px - cxp) * ease;
      cyp += (py - cyp) * ease;
      scale += ((peeking ? 1 : 0.86) - scale) * 0.16;
      peek.style.transform =
        "translate3d(" + (cxp - peek.offsetWidth / 2).toFixed(1) + "px," +
        (cyp - peek.offsetHeight / 2).toFixed(1) + "px,0) scale(" + scale.toFixed(3) + ")";
      requestAnimationFrame(peekLoop);
    })();

    Array.prototype.forEach.call(rows, function (row) {
      row.addEventListener("mouseenter", function () {
        peeking = true;
        peek.classList.add("is-on");
        for (var key in items) items[key].classList.remove("is-on");
        var idx = row.getAttribute("data-peek-i");
        if (items[idx]) items[idx].classList.add("is-on");
      });
      row.addEventListener("mouseleave", function () {
        peeking = false;
        peek.classList.remove("is-on");
      });
    });
  }

  /* ------------------------------------------------ 8. Page transitions */
  var curtain = document.querySelector(".curtain");
  function sameSite(a) {
    if (!a || !a.href) return false;
    if (a.target && a.target !== "_self") return false;
    if (a.hasAttribute("download")) return false;
    var p = a.getAttribute("href") || "";
    if (p.charAt(0) === "#" || p.indexOf("mailto:") === 0 || p.indexOf("tel:") === 0) return false;
    try {
      var u = new URL(a.href, location.href);
      if (u.origin !== location.origin) return false;
      if (u.pathname === location.pathname && u.hash) return false;
      return true;
    } catch (err) { return false; }
  }

  if (curtain && motion) {
    curtain.classList.add("is-out");
    /* Once the reveal has played, park the curtain below the fold and drop the
       animation entirely — a stuck full-screen overlay is the one failure here
       that would take the whole page down. */
    curtain.addEventListener("animationend", function (e) {
      if (e.animationName === "curtainOut") curtain.classList.remove("is-out");
    });
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest("a");
      if (!sameSite(a)) return;
      e.preventDefault();
      curtain.classList.remove("is-out");
      curtain.classList.add("is-in");
      var go = a.href;
      setTimeout(function () { window.location.href = go; }, 480);
    });
    window.addEventListener("pageshow", function (ev) {
      if (ev.persisted) {
        curtain.classList.remove("is-in");
        curtain.classList.add("is-out");
      }
    });
  }

  /* -------------------------------------------------- 10. Current year */
  Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
