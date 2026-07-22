document.addEventListener("DOMContentLoaded", function () {
  var switcher = document.getElementById("research-language-switcher");
  if (!switcher) return;

  var tabs = Array.from(switcher.querySelectorAll(".lang-tab"));
  var panels = Array.from(switcher.querySelectorAll(".lang-panel"));

  function setLanguage(language) {
    document.body.classList.toggle("lang-en", language === "en");
    document.body.classList.toggle("lang-zh", language === "zh");
    document.documentElement.setAttribute("lang", language === "zh" ? "zh-CN" : "en");

    tabs.forEach(function (tab) {
      var active = tab.dataset.lang === language;
      tab.classList.toggle("active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
    });

    panels.forEach(function (panel) {
      panel.classList.toggle("active", panel.dataset.langPanel === language);
    });
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { setLanguage(tab.dataset.lang); });
    tab.addEventListener("mouseenter", function () { setLanguage(tab.dataset.lang); });
    tab.addEventListener("focus", function () { setLanguage(tab.dataset.lang); });
  });

  setLanguage("en");
});
