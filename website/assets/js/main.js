const API_BASE = "https://qadriyat-school-bot.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
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
