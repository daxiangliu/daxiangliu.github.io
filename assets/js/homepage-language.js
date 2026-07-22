document.addEventListener("DOMContentLoaded", function () {
  var switcher = document.querySelector("[data-language-switcher]");
  if (!switcher) return;

  var tabs = Array.from(switcher.querySelectorAll("[data-language]"));
  var panels = Array.from(switcher.querySelectorAll("[data-language-panel]"));

  function selectLanguage(language, focusTab) {
    tabs.forEach(function (tab) {
      var active = tab.dataset.language === language;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
      tab.setAttribute("tabindex", active ? "0" : "-1");
      if (active && focusTab) tab.focus();
    });

    panels.forEach(function (panel) {
      var active = panel.dataset.languagePanel === language;
      panel.classList.toggle("is-active", active);
      panel.hidden = !active;
    });
  }

  tabs.forEach(function (tab, index) {
    tab.addEventListener("click", function () {
      selectLanguage(tab.dataset.language, false);
    });

    tab.addEventListener("keydown", function (event) {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      var direction = event.key === "ArrowRight" ? 1 : -1;
      var nextIndex = (index + direction + tabs.length) % tabs.length;
      selectLanguage(tabs[nextIndex].dataset.language, true);
    });
  });

  selectLanguage("zh", false);
});
