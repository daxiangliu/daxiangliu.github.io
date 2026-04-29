(function () {
  function normalizeLang(raw) {
    if (!raw) return "text";
    var value = raw.toLowerCase();
    if (value === "plain" || value === "plaintext") return "text";
    if (value === "shell" || value === "sh" || value === "zsh" || value === "bash") return "shell";
    return value;
  }

  function detectLang(pre, code) {
    var nodes = [
      code,
      pre,
      pre.parentElement,
      pre.parentElement && pre.parentElement.parentElement,
      pre.closest("[class*='language-']")
    ];

    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      if (!node || !node.classList) continue;
      for (var j = 0; j < node.classList.length; j++) {
        var cls = node.classList[j];
        if (cls.indexOf("language-") === 0) {
          return normalizeLang(cls.slice("language-".length));
        }
      }
    }
    return "text";
  }

  function copyText(text, button) {
    function markCopied() {
      var original = button.textContent;
      button.textContent = "已复制";
      setTimeout(function () {
        button.textContent = original;
      }, 1400);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(markCopied).catch(function () {});
      return;
    }

    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "absolute";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
      markCopied();
    } catch (e) {}
    document.body.removeChild(area);
  }

  function enhanceCodeBlocks() {
    var pres = document.querySelectorAll(".page__content pre");
    pres.forEach(function (pre) {
      if (pre.closest(".codeblock-shell")) return;
      var code = pre.querySelector("code");
      if (!code) return;
      if (code.classList.contains("language-mermaid")) return;

      var lang = detectLang(pre, code);
      var wrapper = pre.closest("div.highlighter-rouge");
      var block = wrapper || pre;

      var shell = document.createElement("div");
      shell.className = "codeblock-shell";
      block.parentNode.insertBefore(shell, block);
      shell.appendChild(block);

      var toolbar = document.createElement("div");
      toolbar.className = "codeblock-toolbar";

      var langTag = document.createElement("span");
      langTag.className = "codeblock-lang";
      langTag.textContent = lang;

      var copyBtn = document.createElement("button");
      copyBtn.className = "codeblock-copy";
      copyBtn.type = "button";
      copyBtn.textContent = "复制";
      copyBtn.addEventListener("click", function () {
        copyText(code.innerText, copyBtn);
      });

      toolbar.appendChild(langTag);
      toolbar.appendChild(copyBtn);
      shell.appendChild(toolbar);
    });
  }

  function enhanceH2() {
    var h2s = document.querySelectorAll(".page__content h2");
    h2s.forEach(function (h2) {
      var firstElement = h2.firstElementChild;
      if (firstElement && firstElement.classList.contains("typora-h2-chip")) return;

      var content = h2.innerHTML;
      var chip = document.createElement("span");
      chip.className = "typora-h2-chip";
      chip.innerHTML = content;
      h2.innerHTML = "";
      h2.appendChild(chip);
    });
  }

  function enhanceToc() {
    var tocMenu = document.querySelector(".sidebar__right .toc__menu");
    if (!tocMenu) return;

    var headings = Array.prototype.slice.call(
      document.querySelectorAll(".page__content h2[id], .page__content h3[id]")
    );

    if (!headings.length) return;

    var lastH2Li = null;
    headings.forEach(function (heading) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + heading.id;
      a.textContent = heading.textContent.trim();
      li.appendChild(a);

      if (heading.tagName === "H2") {
        tocMenu.appendChild(li);
        lastH2Li = li;
        return;
      }

      if (!lastH2Li) {
        tocMenu.appendChild(li);
        return;
      }

      var sub = lastH2Li.querySelector("ul");
      if (!sub) {
        sub = document.createElement("ul");
        sub.className = "toc__sub";
        lastH2Li.appendChild(sub);
      }
      sub.appendChild(li);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    enhanceToc();
    enhanceH2();
    enhanceCodeBlocks();
  });
})();
