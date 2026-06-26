const API_BASE = "https://qadriyat-school-bot.onrender.com";

// Apply saved theme ASAP (before DOMContentLoaded to avoid flicker)
(function () {
  const t = localStorage.getItem("theme");
  if (t) document.documentElement.setAttribute("data-theme", t);
})();

document.addEventListener("DOMContentLoaded", () => {
  initDarkMode();
  initLocationDropdowns();
  initNav();
  initRegistrationForm();
  highlightActiveNav();
  initScrollReveal();
  initFaq();
  initCountUp();
  initScrollTop();
});

function initNav() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    links.classList.toggle("open");
  });

  links.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => links.classList.remove("open"));
  });
}

function highlightActiveNav() {
  const page = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach((link) => {
    const href = link.getAttribute("href").split("#")[0] || "index.html";
    if (href === page) {
      link.classList.add("active");
    }
  });
}

function initRegistrationForm() {
  const form = document.getElementById("registration-form");
  if (!form) return;

  const messageBox = document.getElementById("form-message");
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearErrors(form);
    messageBox.className = "form-message";
    messageBox.textContent = "";

    const payload = {
      full_name: form.full_name.value.trim(),
      phone: form.phone.value.trim(),
      birth_date: formatBirthDate(form.birth_date.value),
      grade: form.grade.value,
      location: form.location.value.trim(),
    };

    submitBtn.disabled = true;
    submitBtn.textContent = "YUBORILMOQDA...";

    try {
      const response = await fetch(`${API_BASE}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await response.json();

      if (result.ok) {
        messageBox.className = "form-message success";
        messageBox.textContent =
          "✅ Arizangiz qabul qilindi! Tez orada operatorlarimiz siz bilan bog'lanishadi.";
        form.reset();
      } else {
        showErrors(form, result.errors || {});
        messageBox.className = "form-message error";
        messageBox.textContent = "⚠️ Iltimos, formadagi xatoliklarni tuzating.";
      }
    } catch (err) {
      messageBox.className = "form-message error";
      messageBox.textContent = "⚠️ Xatolik yuz berdi. Iltimos, birozdan so'ng qaytadan urinib ko'ring.";
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "YUBORISH";
    }
  });
}

function formatBirthDate(isoDate) {
  const parts = isoDate.split("-");
  if (parts.length !== 3) return "";
  const [year, month, day] = parts;
  return `${day}.${month}.${year}`;
}

function showErrors(form, errors) {
  Object.entries(errors).forEach(([field, message]) => {
    const el = form.querySelector(`[data-error-for="${field}"]`);
    if (el) el.textContent = message;
  });
}

function clearErrors(form) {
  form.querySelectorAll(".field-error").forEach((el) => (el.textContent = ""));
}

function initLocationDropdowns() {
  const tumanEl = document.getElementById("tuman");
  const mfyEl   = document.getElementById("mfy");
  const kochaEl = document.getElementById("kocha");
  const locEl   = document.getElementById("location");
  if (!tumanEl || !mfyEl || !locEl) return;

  function updateLocation() {
    const t = tumanEl.value;
    const m = mfyEl.value;
    const k = kochaEl ? kochaEl.value.trim() : "";
    let val = t;
    if (m) val += ", " + m;
    if (k) val += ", " + k;
    locEl.value = val;
  }

  // Populate tuman dropdown
  Object.keys(FARGONA_MFY).forEach((t) => {
    const opt = document.createElement("option");
    opt.value = t;
    opt.textContent = t;
    tumanEl.appendChild(opt);
  });

  tumanEl.addEventListener("change", () => {
    const tuman = tumanEl.value;
    mfyEl.innerHTML = "";
    if (!tuman) {
      mfyEl.disabled = true;
      mfyEl.innerHTML = '<option value="">— Avval tuman tanlang —</option>';
      locEl.value = "";
      return;
    }
    mfyEl.disabled = false;
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "— MFY tanlang —";
    mfyEl.appendChild(placeholder);

    (FARGONA_MFY[tuman] || []).forEach((mfy) => {
      const opt = document.createElement("option");
      opt.value = mfy;
      opt.textContent = mfy;
      mfyEl.appendChild(opt);
    });
    locEl.value = "";
  });

  mfyEl.addEventListener("change", updateLocation);
  if (kochaEl) kochaEl.addEventListener("input", updateLocation);
}

function initDarkMode() {
  const btn = document.getElementById("dark-toggle");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });
}

// lang switcher removed
const LANGS_UNUSED = {
  uz: {
    "nav.home":       "Bosh sahifa",
    "nav.about":      "Biz haqimizda",
    "nav.edu":        "Ta'lim",
    "nav.facilities": "Sharoitlar",
    "nav.contact":    "Bog'lanish",
    "nav.register":   "Ro'yxatdan o'tish",
    "nav.news":       "Yangiliklar",
    "hero.title":     "Farzandingiz uchun sifatli ta'lim va mustahkam tarbiya",
    "hero.sub":       "Jahon tillari va matematikaga ixtisoslashtirilgan zamonaviy xususiy maktab. 1-sinfdan 11-sinfgacha bo'lgan o'quvchilarimizga xalqaro standartlardagi ta'lim va g'amxo'r tarbiyani taqdim etamiz.",
    "hero.about":     "Biz haqimizda",
    "sec.why":        "Nima uchun bizni tanlaymiz?",
    "sec.reg":        "Ro'yxatdan o'tish",
    "sec.contact":    "Bog'lanish",
    "sec.faq":        "Ko'p so'raladigan savollar",
    "btn.consult":    "Suhbatga yozilish",
    "btn.channel":    "Kanalga a'zo bo'lish",
    "btn.tg":         "Telegramda ochish",
  },
  ru: {
    "nav.home":       "Главная",
    "nav.about":      "О нас",
    "nav.edu":        "Обучение",
    "nav.facilities": "Условия",
    "nav.contact":    "Контакты",
    "nav.register":   "Записаться",
    "nav.news":       "Новости",
    "hero.title":     "Качественное образование и воспитание для вашего ребёнка",
    "hero.sub":       "Современная частная школа с углублённым изучением мировых языков и математики. Обучение с 1 по 11 класс по международным стандартам.",
    "hero.about":     "О нас",
    "sec.why":        "Почему выбирают нас?",
    "sec.reg":        "Записаться",
    "sec.contact":    "Контакты",
    "sec.faq":        "Часто задаваемые вопросы",
    "btn.consult":    "Записаться на собеседование",
    "btn.channel":    "Подписаться на канал",
    "btn.tg":         "Открыть в Telegram",
  },
  en: {
    "nav.home":       "Home",
    "nav.about":      "About Us",
    "nav.edu":        "Education",
    "nav.facilities": "Facilities",
    "nav.contact":    "Contact",
    "nav.register":   "Register",
    "nav.news":       "News",
    "hero.title":     "Quality Education and Upbringing for Your Child",
    "hero.sub":       "A modern private school specialising in world languages and mathematics. Education from grade 1 to 11 by international standards.",
    "hero.about":     "About Us",
    "sec.why":        "Why choose us?",
    "sec.reg":        "Register",
    "sec.contact":    "Contact",
    "sec.faq":        "Frequently Asked Questions",
    "btn.consult":    "Book a Consultation",
    "btn.channel":    "Join our channel",
    "btn.tg":         "Open in Telegram",
  },
};


function initCountUp() {
  if (!("IntersectionObserver" in window)) return;
  const nums = document.querySelectorAll(".stat-number[data-target]");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.target);
      const suffix = el.dataset.suffix || "";
      let current = 0;
      const step = target / 60;
      const timer = setInterval(() => {
        current += step;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        el.textContent = Math.floor(current) + suffix;
      }, 16);
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });
  nums.forEach((el) => observer.observe(el));
}

function initScrollTop() {
  const btn = document.getElementById("scroll-top");
  if (!btn) return;
  window.addEventListener("scroll", () => {
    btn.classList.toggle("visible", window.scrollY > 400);
  });
  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

function initFaq() {
  document.querySelectorAll(".faq-question").forEach((btn) => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".faq-item");
      const isOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach((el) => el.classList.remove("open"));
      if (!isOpen) item.classList.add("open");
    });
  });
}

function initScrollReveal() {
  if (!("IntersectionObserver" in window)) return;

  const targets = document.querySelectorAll(
    ".card, .section-header, .split, .testimonial, .cta-banner, .contact-grid, .reg-card, .gallery-grid"
  );

  targets.forEach((el, i) => {
    el.classList.add("reveal");
    if (i % 3 === 1) el.classList.add("reveal-delay-1");
    if (i % 3 === 2) el.classList.add("reveal-delay-2");
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  targets.forEach((el) => observer.observe(el));
}
