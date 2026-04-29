/* ==========================================================================
   模板中会复用的通用函数
   ========================================================================== */

// 读取主题开关的期望状态，可为 "dark"、"light" 或 "system"。
// 默认值为 "system"。
let determineThemeSetting = () => {
  let themeSetting = localStorage.getItem("theme");
  return (themeSetting != "dark" && themeSetting != "light" && themeSetting != "system") ? "system" : themeSetting;
};

// 计算当前应使用的主题（"dark" 或 "light"）。
// 当设置为 "system" 时，按系统偏好自动判断。
let determineComputedTheme = () => {
  let themeSetting = determineThemeSetting();
  if (themeSetting != "system") {
    return themeSetting;
  }
  return (userPref && userPref("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
};

// 检测操作系统/浏览器主题偏好
const browserPref = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

// 页面加载或显式调用时设置主题
let setTheme = (theme) => {
  const use_theme =
    theme ||
    localStorage.getItem("theme") ||
    $("html").attr("data-theme") ||
    browserPref;

  if (use_theme === "dark") {
    $("html").attr("data-theme", "dark");
    $("#theme-icon").removeClass("fa-sun").addClass("fa-moon");
  } else if (use_theme === "light") {
    $("html").removeAttr("data-theme");
    $("#theme-icon").removeClass("fa-moon").addClass("fa-sun");
  }
};

// 手动切换主题
var toggleTheme = () => {
  const current_theme = $("html").attr("data-theme");
  const new_theme = current_theme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", new_theme);
  setTheme(new_theme);
};

/* ==========================================================================
   Plotly 集成：将 Markdown 代码块渲染为图表
   ========================================================================== */

// 读取代码块中的 Plotly 数据，隐藏原代码块，并渲染为新图表节点。
// 这样在切换主题时仍可重新读取 JSON 数据。
// 仅当页面中存在相关数据时才注册监听器。
import { plotlyDarkLayout, plotlyLightLayout } from './theme.js';
let plotlyElements = document.querySelectorAll("pre>code.language-plotly");
if (plotlyElements.length > 0) {
  document.addEventListener("readystatechange", () => {
    if (document.readyState === "complete") {
      plotlyElements.forEach((elem) => {
        // 解析 Plotly JSON 并隐藏原始代码块
        var jsonData = JSON.parse(elem.textContent);
        elem.parentElement.classList.add("hidden");

        // 添加图表容器节点
        let chartElement = document.createElement("div");
        elem.parentElement.after(chartElement);

        // 设置图表主题并渲染
        const theme = (determineComputedTheme() === "dark") ? plotlyDarkLayout : plotlyLightLayout;
        if (jsonData.layout) {
          jsonData.layout.template = (jsonData.layout.template) ? { ...theme, ...jsonData.layout.template } : theme;
        } else {
          jsonData.layout = { template: theme };
        }
        Plotly.react(chartElement, jsonData.data, jsonData.layout);
      });
    }
  });
}

/* ==========================================================================
   页面完全加载后要执行的动作
   ========================================================================== */

$(document).ready(function () {
  // SCSS 设置：需与相关样式文件中的值保持一致
  const scssLarge = 925;          // pixels, from /_sass/_themes.scss
  const scssMastheadHeight = 70;  // pixels, from the current theme (e.g., /_sass/theme/_default.scss)

  // 用户未手动选择主题时，跟随系统主题
  setTheme();
  window.matchMedia('(prefers-color-scheme: dark)')
        .addEventListener("change", (e) => {
          if (!localStorage.getItem("theme")) {
            setTheme(e.matches ? "dark" : "light");
          }
        });

  // 启用主题切换按钮
  $('#theme-toggle').on('click', toggleTheme);

  // 启用粘性页脚
  var bumpIt = function () {
    $("body").css("padding-bottom", "0");
    $("body").css("margin-bottom", $(".page__footer").outerHeight(true));
  }
  $(window).resize(function () {
    didResize = true;
  });
  setInterval(function () {
    if (didResize) {
      didResize = false;
      bumpIt();
    }}, 250);
  var didResize = false;
  bumpIt();

  // 初始化 FitVids
  fitvids();

  // 关注菜单下拉
  $(".author__urls-wrapper button").on("click", function () {
    $(".author__urls").fadeToggle("fast", function () { });
    $(".author__urls-wrapper button").toggleClass("open");
  });

  // 若窗口变化导致样式切换，恢复关注菜单状态
  jQuery(window).on('resize', function () {
    if ($('.author__urls.social-icons').css('display') == 'none' && $(window).width() >= scssLarge) {
      $(".author__urls").css('display', 'block')
    }
  });

  // 初始化平滑滚动，偏移量略大于固定头部高度
  $("a").smoothScroll({
    offset: -scssMastheadHeight,
    preventDefault: false,
  });

});
