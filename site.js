/* ==========================================================================
   AKINTAYO — sports web design
   Vanilla JS, no dependencies. Everything here is an enhancement: the pages
   are complete and readable with this file absent, and every motion is
   switched off under prefers-reduced-motion.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* .js lets CSS hide things that JS will reveal. Only set it when motion is
     allowed, so a reduced-motion visitor never gets a hidden element. */
  root.classList.add("js");
  if (!reduced) root.classList.add("anim");

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* --------------------------------------------------------- live clock */
  function clock() {
    var els = $$("[data-clock]");
    if (!els.length) return;
    var f = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Africa/Lagos", hour: "2-digit", minute: "2-digit", hour12: true
    });
    var t = f.format(new Date()).toUpperCase().replace(/\s+/g, " ");
    els.forEach(function (el) { el.textContent = t + " GMT+1"; });
  }
  clock();
  setInterval(clock, 30000);

  /* ------------------------------------------------------------- header */
  var hdr = $(".hdr");
  if (hdr && !hdr.classList.contains("hdr--static")) {
    var last = 0;
    window.addEventListener("scroll", function () {
      var y = window.scrollY;
      hdr.classList.toggle("is-stuck", y > 80);
      hdr.classList.toggle("is-up", y > 220 && y > last);
      last = y;
    }, { passive: true });
  }

  /* -------------------------------------------------------- mobile menu */
  var menu = $(".menu"), burger = $(".burger");
  if (menu && burger) {
    var closeBtn = $(".menu__close", menu), lastFocus = null;
    function openMenu() {
      lastFocus = document.activeElement;
      menu.classList.add("is-open");
      menu.removeAttribute("inert");
      burger.setAttribute("aria-expanded", "true");
      root.style.overflow = "hidden";
      (closeBtn || menu).focus();
      document.addEventListener("keydown", menuKey, true);
    }
    function closeMenu() {
      menu.classList.remove("is-open");
      menu.setAttribute("inert", "");
      burger.setAttribute("aria-expanded", "false");
      root.style.overflow = "";
      document.removeEventListener("keydown", menuKey, true);
      if (lastFocus) lastFocus.focus();
    }
    function menuKey(e) {
      if (e.key === "Escape") { e.preventDefault(); closeMenu(); return; }
      if (e.key !== "Tab") return;
      var f = $$("a,button", menu);
      if (!f.length) return;
      var first = f[0], lastEl = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); lastEl.focus(); }
      else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); first.focus(); }
    }
    menu.setAttribute("inert", "");
    burger.addEventListener("click", openMenu);
    if (closeBtn) closeBtn.addEventListener("click", closeMenu);
  }

  /* ------------------------------------------------- marquee duplication
     Duplicate the track once so the -100% loop has something to run into. */
  if (!reduced) {
    $$(".mq__t, .mqv__t").forEach(function (t) {
      var clone = t.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      t.parentNode.appendChild(clone);
    });
  }

  /* -------------------------------------------------------- scroll reveal */
  var revealables = $$("[data-reveal]");
  var hero = $(".hero");
  if (!("IntersectionObserver" in window) || reduced) {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
    if (hero) hero.classList.add("is-in");
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var sibs = el.parentNode ? $$("[data-reveal]", el.parentNode) : [];
        var i = sibs.indexOf(el);
        el.style.transitionDelay = (i > 0 ? Math.min(i, 6) * 0.1 : 0) + "s";
        el.classList.add("is-in");
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -15% 0px" });
    revealables.forEach(function (el) { io.observe(el); });
    if (hero) requestAnimationFrame(function () { hero.classList.add("is-in"); });
  }

  /* ----------------------------------------------------- count-up numbers
     The final value stays in the HTML, so no-JS and screen readers get it. */
  $$("[data-count]").forEach(function (el) {
    var finalText = el.textContent;
    var target = parseFloat(el.getAttribute("data-count"));
    if (isNaN(target) || reduced || !("IntersectionObserver" in window)) return;
    var pre = el.getAttribute("data-pre") || "";
    var post = el.getAttribute("data-post") || "";
    var ob = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return;
      ob.disconnect();
      var t0 = null, dur = 1400;
      function tick(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + Math.round(target * eased) + post;
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = finalText;
      }
      requestAnimationFrame(tick);
    }, { rootMargin: "0px 0px -20% 0px" });
    ob.observe(el);
  });

  /* -------------------------------------------------- sports row preview */
  if (!reduced && window.matchMedia("(hover: hover)").matches) {
    $$(".srow").forEach(function (row) {
      var prev = $(".srow__prev", row);
      if (!prev) return;
      row.addEventListener("mousemove", function (e) {
        var r = row.getBoundingClientRect();
        var dy = (e.clientY - r.top - r.height / 2) * 0.12;
        prev.style.marginTop = dy.toFixed(1) + "px";
      });
      row.addEventListener("mouseleave", function () { prev.style.marginTop = "0px"; });
    });
  }

  /* ------------------------------------------------------- work filter */
  var filters = $(".filters");
  if (filters) {
    var cards = $$("[data-sport]");
    filters.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      var want = btn.getAttribute("data-filter");
      $$("button", filters).forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === btn));
      });
      cards.forEach(function (c) { c.classList.add("is-fade"); });
      setTimeout(function () {
        cards.forEach(function (c) {
          var show = want === "all" || c.getAttribute("data-sport") === want;
          c.classList.toggle("is-out", !show);
        });
        requestAnimationFrame(function () {
          cards.forEach(function (c) { c.classList.remove("is-fade"); });
        });
      }, reduced ? 0 : 200);
    });
  }

  /* --------------------------------------------------- video lightbox */
  var vtrigger = $("[data-video]");
  var dlg = $("#videoDialog");
  if (vtrigger && dlg && typeof dlg.showModal === "function") {
    var vid = $("video", dlg);
    vtrigger.addEventListener("click", function () {
      dlg.showModal();
      if (vid) { try { vid.play(); } catch (err) {} }
    });
    var x = $(".lbx__x", dlg);
    if (x) x.addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () {
      if (vid) { vid.pause(); vid.currentTime = 0; }
      vtrigger.focus();
    });
  }

  /* -------------------------------------------------- contact → mailto */
  var form = $("#projectForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var body = [
        "My website: " + (d.get("site") || ""),
        "My sport and business: " + (d.get("biz") || ""),
        "",
        "What is not working:",
        (d.get("problem") || ""),
        "",
        "Timeline: " + (d.get("when") || "")
      ].join("\n");
      window.location.href = "mailto:akintayo@akintayoakingbehin.com"
        + "?subject=" + encodeURIComponent("Website project enquiry")
        + "&body=" + encodeURIComponent(body);
    });
  }

  /* -------------------------------------------------- mobile sticky bar */
  var sticky = $(".sticky");
  if (sticky) {
    window.addEventListener("scroll", function () {
      sticky.classList.toggle("is-on", window.scrollY > (window.innerHeight * 0.7));
    }, { passive: true });
  }

  /* ------------------------------------- before / after comparison slider */
  Array.prototype.forEach.call(document.querySelectorAll(".ba"), function (ba) {
    var r = ba.querySelector(".ba__range");
    if (!r) return;
    function set() { ba.style.setProperty("--pos", r.value + "%"); }
    r.addEventListener("input", set);
    set();
  });

  /* --------------------------------------------- ball trail on the cursor */
  if (!reduced && window.matchMedia("(hover:hover) and (pointer:fine)").matches) {
    var bLast = null, bAcc = 0, bFlip = 0, bLive = 0;
    document.addEventListener("pointermove", function (e) {
      if (e.pointerType && e.pointerType !== "mouse") return;
      if (!bLast) { bLast = [e.clientX, e.clientY]; return; }
      var dx = e.clientX - bLast[0], dy = e.clientY - bLast[1];
      bAcc += Math.sqrt(dx * dx + dy * dy);
      bLast = [e.clientX, e.clientY];
      if (bAcc < 135 || bLive > 7) return;
      bAcc = 0; bLive++;
      var d = document.createElement("span");
      d.className = "bdot " + (bFlip++ % 3 === 2 ? "bdot--fb" : "bdot--tt");
      var sz = Math.round(9 + Math.random() * 9);
      d.style.cssText = "--s:" + sz + "px;left:" + e.clientX + "px;top:" + e.clientY + "px";
      document.body.appendChild(d);
      d.addEventListener("animationend", function () { d.remove(); bLive--; });
    }, { passive: true });
  }

  /* ------------------------------------------------------ page transition */
  if (!reduced) {
    var mesh = "";
    for (var mx = 36; mx < 240; mx += 20) mesh += '<path d="M' + mx + ' 18V162"/>';
    for (var my = 36; my < 162; my += 20) mesh += '<path d="M20 ' + my + 'H220"/>';

    var curtain = document.createElement("div");
    curtain.className = "curtain out";
    curtain.setAttribute("aria-hidden", "true");
    curtain.innerHTML =
      '<span class="curtain__bg"></span>' +
      '<svg class="curtain__goal" viewBox="0 0 240 172" fill="none">' +
        '<g class="curtain__net" stroke="currentColor" stroke-opacity=".32" stroke-width="1.5">' +
          mesh +
        '</g>' +
        '<path d="M20 164V18h200v146" stroke="currentColor" stroke-width="11" ' +
          'stroke-linecap="round" stroke-linejoin="round"/>' +
      '</svg>' +
      '<span class="curtain__ball"><span><i></i></span></span>';
    document.body.appendChild(curtain);
    curtain.addEventListener("animationend", function () {
      if (curtain.classList.contains("out")) curtain.classList.remove("out", "in");
    });

    document.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (!a) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      var href = a.getAttribute("href") || "";
      if (!href || href.charAt(0) === "#" || a.target === "_blank"
          || href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0
          || a.hasAttribute("download") || a.hostname !== window.location.hostname) return;
      e.preventDefault();
      curtain.classList.remove("out");
      curtain.classList.add("in");
      setTimeout(function () { window.location.href = href; }, 640);
    });
  }
})();
