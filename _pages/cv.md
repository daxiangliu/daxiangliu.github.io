---
layout: archive
title: "简历"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

教育背景
======
* [学历]，[学校]，[年份]
* [学历]，[学校]，[年份]
* [学历]，[学校]，[年份]

工作经历
======
* [时间]：[职位]
  * [单位]
  * [职责]
  * [主管/合作导师（可选）]

* [时间]：[职位]
  * [单位]
  * [职责]

* [时间]：[职位]
  * [单位]
  * [职责]
  
技能
======
* [技能 1]
* [技能 2]
* [技能 3]

论文与出版物
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
演讲与报告
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
  
教学经历
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
服务与领导力
======
* [学术服务、社区贡献或团队协作经历]
