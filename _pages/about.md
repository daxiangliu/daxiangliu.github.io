---
permalink: /
title: ""
excerpt: "Daxiang Liu，深圳大学计算机科学与技术硕士研究生，研究方向包括 Text-to-CAD 跨模态检索、CAD 表示学习与生成，以及医学图像分析。"
author_profile: true
classes:
  - homepage-page
custom_css:
  - /assets/css/homepage.css
redirect_from:
  - /about/
  - /about.html
---

<div class="home-shell">
  <section class="home-hero" aria-labelledby="home-title">
    <div class="home-hero__copy">
      <p class="home-eyebrow">Daxiang Liu · Academic Homepage</p>
      <h1 id="home-title">CAD / 3D 智能与<br>多模态学习</h1>
      <p class="home-lead">你好，我是 Daxiang Liu，目前在深圳大学攻读计算机科学与技术硕士学位。我的研究以 <strong>CAD / 3D 智能</strong>为主线，关注跨模态检索、表示学习与生成，并探索人工智能在医学图像分析中的应用。</p>
      <div class="home-actions" aria-label="主要链接">
        <a class="home-button home-button--primary" href="{{ '/publications/' | relative_url }}">查看研究成果 <span aria-hidden="true">→</span></a>
        <a class="home-button" href="https://github.com/daxiangliu" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a class="home-button" href="{{ '/cv/' | relative_url }}">CV</a>
      </div>
      <p class="home-affiliation"><span aria-hidden="true"></span> Shenzhen University · Shenzhen, China</p>
    </div>

    <aside class="research-summary" aria-labelledby="current-focus-title">
      <p class="research-summary__label">Current focus</p>
      <h2 id="current-focus-title">Text-to-CAD Retrieval</h2>
      <p class="research-summary__intro">用自然语言从大规模三维模型库中检索语义相关、可复用的 CAD 模型。</p>
      <dl class="research-summary__list">
        <div><dt>01</dt><dd>跨模态检索</dd></div>
        <div><dt>02</dt><dd>CAD 表示学习</dd></div>
        <div><dt>03</dt><dd>三维模型生成</dd></div>
      </dl>
      <p class="research-summary__footer">Natural language · CAD sequence · 3D geometry</p>
    </aside>
  </section>

  <section class="home-section" aria-labelledby="focus-title">
    <div class="section-heading">
      <div>
        <p class="section-kicker">Research focus</p>
        <h2 id="focus-title">研究方向</h2>
      </div>
      <p>从设计语义到几何结构，研究多模态信息如何共同描述、检索并生成复杂对象。</p>
    </div>

    <div class="focus-grid">
      <article class="focus-card focus-card--primary">
        <div class="focus-card__index">01 / CORE</div>
        <h3>CAD / 3D Intelligence</h3>
        <p>围绕工程设计模型的检索、理解与生成，连接自然语言、构造序列和三维几何表示。</p>
        <ul>
          <li>Text-to-CAD 跨模态检索</li>
          <li>CAD 表示学习与生成</li>
          <li>多模态几何理解</li>
        </ul>
      </article>

      <article class="focus-card">
        <div class="focus-card__index">02 / APPLIED</div>
        <h3>Medical AI</h3>
        <p>面向临床影像的结构化理解，让模型输出更具可解释性、可核查性与实际应用价值。</p>
        <ul>
          <li>医学图像分析</li>
          <li>解剖感知表征</li>
          <li>结构化影像报告</li>
        </ul>
      </article>
    </div>
  </section>

  <section class="home-section" aria-labelledby="work-title">
    <div class="section-heading section-heading--works">
      <div>
        <p class="section-kicker">Selected work</p>
        <h2 id="work-title">代表工作</h2>
      </div>
      <a class="section-link" href="{{ '/publications/' | relative_url }}">全部论文 <span aria-hidden="true">→</span></a>
    </div>

    <div class="work-list">
      <article class="work-card">
        <div class="work-card__visual work-card__visual--cad" aria-hidden="true">
          <div class="cad-preview__label">TEXT-TO-CAD / RETRIEVAL</div>
          <div class="cad-preview__query">natural language query</div>
          <div class="cad-preview__line"></div>
          <div class="cad-preview__results">
            <span></span><span></span><span></span>
          </div>
        </div>
        <div class="work-card__body">
          <div class="work-card__meta"><span>arXiv 2026</span><span>Cross-modal Retrieval</span></div>
          <h3>Text-to-CAD Retrieval: a Strong Baseline</h3>
          <p>从自然语言描述中检索语义相关的三维 CAD 模型，并联合构造序列与几何点云建立统一检索基线。</p>
          <p class="work-card__authors">Honghu Pan, Zibo Du, <strong>Daxiang Liu</strong>, Chengliang Liu, Xiaoling Luo</p>
          <div class="work-card__links">
            <a href="https://arxiv.org/abs/2605.05572" target="_blank" rel="noopener noreferrer">Paper ↗</a>
            <a href="{{ '/publication/text-to-cad-retrieval/' | relative_url }}">Project →</a>
          </div>
        </div>
      </article>

      <article class="work-card">
        <div class="work-card__visual work-card__visual--image">
          <img src="{{ '/assets/projects/medstrucgen/framework.png' | relative_url }}" alt="MedStrucGen-ML 方法框架图" loading="lazy">
        </div>
        <div class="work-card__body">
          <div class="work-card__meta"><span>Under Review</span><span>Medical AI</span></div>
          <h3>Structured Radiology Report Generation for Temporomandibular Disorders</h3>
          <p>通过检测引导的局部表征与类别特定交叉注意力，生成结构化、可核查的颞下颌关节影像报告。</p>
          <div class="work-card__links">
            <a href="https://github.com/daxiangliu/MedStrucGen-ML" target="_blank" rel="noopener noreferrer">Code ↗</a>
            <a href="{{ '/publication/medstrucgen-ml/' | relative_url }}">Project →</a>
          </div>
        </div>
      </article>
    </div>
  </section>

  <section class="home-section home-section--split" aria-label="最新动态与个人简介">
    <div class="news-panel">
      <div class="section-heading section-heading--compact">
        <div>
          <p class="section-kicker">Updates</p>
          <h2>最新动态</h2>
        </div>
      </div>
      <ol class="news-list">
        <li>
          <time datetime="2026-05">2026.05</time>
          <p><a href="{{ '/publication/text-to-cad-retrieval/' | relative_url }}">Text-to-CAD Retrieval</a> 已公开为 arXiv 预印本。</p>
        </li>
        <li>
          <time datetime="2026-04">2026.04</time>
          <p><a href="{{ '/publication/medstrucgen-ml/' | relative_url }}">MedStrucGen-ML</a> 项目页与代码仓库已公开。</p>
        </li>
      </ol>
    </div>

    <aside class="about-panel">
      <p class="section-kicker">Beyond research</p>
      <h2>研究之外</h2>
      <p>本科毕业于哈尔滨理工大学软件工程专业。研究之外，我喜欢旅行与摄影，也会记录一些学习过程和技术实践。</p>
      <div class="about-panel__links">
        <a href="{{ '/year-archive/' | relative_url }}">阅读文章</a>
        <a href="mailto:liudaxiang.cs@foxmail.com">联系我</a>
      </div>
    </aside>
  </section>
</div>
