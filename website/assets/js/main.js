const API_BASE = "https://qadriyat-school-bot.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  initRegistrationForm();
  highlightActiveNav();
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

function showErrors(form, errors) {
  Object.entries(errors).forEach(([field, message]) => {
    const el = form.querySelector(`[data-error-for="${field}"]`);
    if (el) el.textContent = message;
  });
}

function clearErrors(form) {
  form.querySelectorAll(".field-error").forEach((el) => (el.textContent = ""));
}
