(() => {
  const root = document.documentElement;
  const themeToggle = document.querySelector(".theme-toggle");
  const savedTheme = localStorage.getItem("medstrucgen-theme");

  function applyTheme(theme) {
    root.dataset.theme = theme;
    const dark = theme === "dark";
    themeToggle?.setAttribute("aria-pressed", String(dark));
    themeToggle?.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
  }

  applyTheme(savedTheme || "light");
  themeToggle?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    localStorage.setItem("medstrucgen-theme", next);
    applyTheme(next);
  });

  const toast = document.querySelector(".toast");
  let toastTimer;
  function showToast(message, title = "Coming soon") {
    if (!toast) return;
    toast.querySelector("strong").textContent = title;
    toast.querySelector("span").textContent = message;
    toast.setAttribute("aria-hidden", "false");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.setAttribute("aria-hidden", "true"), 3400);
  }

  document.querySelectorAll("[data-coming-soon]").forEach((button) => {
    button.addEventListener("click", () => showToast(button.dataset.comingSoon));
  });

  document.querySelector(".copy-citation")?.addEventListener("click", async (event) => {
    try {
      await navigator.clipboard.writeText(event.currentTarget.dataset.citation);
      showToast("The citation has been copied to your clipboard.", "Copied");
    } catch (_) {
      showToast("Clipboard access is unavailable. Please select the citation manually.", "Copy unavailable");
    }
  });

  const header = document.querySelector(".project-header");
  window.addEventListener("scroll", () => header?.classList.toggle("scrolled", window.scrollY > 12), { passive: true });
})();
