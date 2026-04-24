---
permalink: /
title: "Kareem Hegazy"
excerpt: "Postdoctoral researcher at UC Berkeley / Berkeley Lab / ICSI. Physics PhD from Stanford."
author_profile: false
classes: wide-page
redirect_from:
  - /about/
  - /about.html
---

<style>
/* ------------------------------------------------------------------
   Homepage-only layout overrides:
   - Hide the theme's <h1 class="page__title"> (our hero renders the name)
   - Let the content take the full width of #main (no 2/12 right gutter)
   - Keep #main centered but trim its internal padding so margins are
     narrower without the page feeling cramped.
   ------------------------------------------------------------------ */
.page__title { display: none; }
#main {
  max-width: 1100px;
  padding-left: 1.5em;
  padding-right: 1.5em;
}
.page {
  float: none !important;
  width: 100% !important;
  max-width: 100% !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}

/* ------------------------------------------------------------------
   Homepage hero (photo left, bio right — scrolls with the page)
   ------------------------------------------------------------------ */
.hero {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  margin: 0.5em 0 2em 0;
}
.hero__image {
  flex: 0 0 auto;
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid #e5e5e5;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.hero__text { flex: 1 1 auto; min-width: 0; }
.hero__name {
  margin: 0 0 0.15em 0;
  font-weight: 700;
  font-size: 2.2em;
  line-height: 1.1;
}
.hero__subtitle {
  margin: 0 0 1em 0;
  color: #555;
  font-size: 1.05em;
  font-weight: 400;
}
.hero__bio { font-size: 1em; line-height: 1.6; }
.hero__bio p { margin: 0 0 0.9em 0; }
@media (max-width: 700px) {
  .hero { flex-direction: column; align-items: center; text-align: left; }
  .hero__image { width: 160px; height: 160px; }
  .hero__text { width: 100%; }
  .hero__name { font-size: 1.9em; }
}

/* ------------------------------------------------------------------
   Section headings on the homepage
   ------------------------------------------------------------------ */
.page__content h1,
.page__content h2 {
  margin-top: 2.25em;
  padding-bottom: 0.25em;
  border-bottom: 1px solid #eee;
}

/* ------------------------------------------------------------------
   Clickable publication card — title / authors / venue / description
   ------------------------------------------------------------------ */
.pub-link-card {
  position: relative;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  padding: 0.9rem 1.15rem 0.75rem 1.15rem;
  margin: 0.7rem 0;
  transition: background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}
.pub-link-card:hover {
  background: #fafafa;
  border-color: #c9c9c9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.pub-link-card .pub-title {
  margin: 0 0 0.3em 0;
  font-weight: 600;
  font-size: 1.05em;
  line-height: 1.3;
}
.pub-link-card .pub-title a {
  color: #222;
  text-decoration: none;
}
/* "Stretched link" — makes the card clickable via the title anchor.
   Action buttons below have a higher z-index so they remain clickable. */
.pub-link-card .pub-title a::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
}
.pub-link-card:hover .pub-title a { text-decoration: underline; }
.pub-link-card .pub-authors {
  margin: 0.1em 0;
  font-size: 0.95em;
  color: #444;
}
.pub-link-card .pub-venue {
  margin: 0.1em 0;
  font-size: 0.9em;
  color: #666;
  font-style: italic;
}
.pub-link-card .pub-excerpt {
  margin: 0.5em 0 0 0;
  font-size: 0.95em;
  color: #333;
  line-height: 1.5;
}

/* Action buttons — arXiv / Paper / Code / Blog */
.pub-link-card .pub-actions {
  position: relative;
  z-index: 2;            /* above the stretched title link */
  margin: 0.6em 0 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.pub-link-card .pub-action {
  display: inline-block;
  padding: 0.15em 0.7em;
  font-size: 0.82em;
  font-weight: 500;
  color: #333 !important;
  background: #f3f4f6;
  border: 1px solid #d9dbe0;
  border-radius: 4px;
  text-decoration: none !important;
}
.pub-link-card .pub-action:hover {
  background: #e9ebf0;
  border-color: #bfc3cc;
  color: #111 !important;
}

/* ------------------------------------------------------------------
   Blog card (with thumbnail)
   ------------------------------------------------------------------ */
.pub-card { display: flex; gap: 1.25rem; align-items: flex-start; margin: 1.25rem 0; }
.pub-card .pub-thumb { width: 180px; max-width: 30%; flex-shrink: 0; border-radius: 4px; }
.pub-card .pub-body { flex: 1; min-width: 0; }
.pub-card h4 { margin: 0 0 0.35em 0; font-weight: 600; }
.pub-card .pub-excerpt { color: #444; font-style: italic; margin: 0.25em 0 0.5em 0; }
.pub-card .pub-venue { margin: 0.15em 0; font-size: 0.95em; color: #555; }

.empty-state { color: #777; font-style: italic; padding: 0.75rem 0; }

@media (max-width: 600px) {
  .pub-card { flex-direction: column; }
  .pub-card .pub-thumb { width: 100%; max-width: 100%; }
}
</style>

<section class="hero">
  <img class="hero__image" src="{{ '/images/profile.png' | relative_url }}" alt="Kareem Hegazy"/>
  <div class="hero__text">
    <h1 class="hero__name">Kareem Hegazy</h1>
    <p class="hero__subtitle">Postdoctoral Researcher · UC Berkeley · Lawrence Berkeley National Lab · ICSI</p>
    <div class="hero__bio" markdown="1">
I am a postdoctoral researcher at [UC Berkeley](https://statistics.berkeley.edu/), [Lawrence Berkeley National Lab](https://www.lbl.gov/), and [ICSI](https://www.icsi.berkeley.edu/icsi/), working with [Michael Mahoney](https://www.stat.berkeley.edu/~mmahoney/) and [Benjamin Erichson](https://www.benerichson.com/) at the intersection of Physics, Chemistry, and AI. I received my Physics PhD from Stanford in 2023 under [Phil Bucksbaum](https://physics.stanford.edu/people/philip-bucksbaum) and [Ryan Coffee](https://profiles.stanford.edu/ryan-coffee), where I studied excited-state quantum molecular dynamics through [ultrafast gas-phase diffraction](https://lcls.slac.stanford.edu/instruments/mev-ued). In summer 2019 I was an AI Research Fellow at Google X on the [Blueshift team](https://research.google/teams/blueshift/). I previously earned an Honors B.Sc. in Physics and Math from the University of Michigan, where I researched the Higgs Boson at CERN with [Bing Zhou](https://lsa.umich.edu/physics/people/faculty/bzhou.html).

I am broadly interested in the intersection of physics and machine learning — LLMs for time series, ML for thermodynamic processes and PDE modeling, ML chemical potentials, and inverse problems.
    </div>
  </div>
</section>

<h1 id="publications">Selected Publications</h1>

<div class="pubs-list">
{% assign featured_pubs = site.publications | where: "featured", true | sort: "date" | reverse %}
{% if featured_pubs.size > 0 %}
  {% for pub in featured_pubs %}
    {% if pub.paperurl and pub.paperurl != "" %}
      {% assign pub_href = pub.paperurl %}
    {% elsif pub.arxivurl and pub.arxivurl != "" %}
      {% assign pub_href = pub.arxivurl %}
    {% else %}
      {% assign pub_href = pub.permalink | relative_url %}
    {% endif %}
<div class="pub-link-card" markdown="0">
  <h4 class="pub-title"><a href="{{ pub_href }}">{{ pub.title }}</a></h4>
  {% if pub.authors %}<p class="pub-authors">{{ pub.authors }}</p>{% endif %}
  {% if pub.venue %}<p class="pub-venue">{{ pub.venue }}</p>{% endif %}
  {% if pub.excerpt %}<p class="pub-excerpt">{{ pub.excerpt | strip_html }}</p>{% endif %}
  {% assign has_actions = false %}
  {% if pub.arxivurl and pub.arxivurl != "" %}{% assign has_actions = true %}{% endif %}
  {% if pub.paperurl and pub.paperurl != "" %}{% assign has_actions = true %}{% endif %}
  {% if pub.codeurl and pub.codeurl != "" %}{% assign has_actions = true %}{% endif %}
  {% if pub.blogurl and pub.blogurl != "" %}{% assign has_actions = true %}{% endif %}
  {% if has_actions %}
  <p class="pub-actions">
    {% if pub.arxivurl and pub.arxivurl != "" %}<a class="pub-action" href="{{ pub.arxivurl }}" rel="noopener">arXiv</a>{% endif %}
    {% if pub.paperurl and pub.paperurl != "" %}<a class="pub-action" href="{{ pub.paperurl }}" rel="noopener">Paper</a>{% endif %}
    {% if pub.codeurl and pub.codeurl != "" %}<a class="pub-action" href="{{ pub.codeurl }}" rel="noopener">Code</a>{% endif %}
    {% if pub.blogurl and pub.blogurl != "" %}<a class="pub-action" href="{{ pub.blogurl }}" rel="noopener">Blog</a>{% endif %}
  </p>
  {% endif %}
</div>
  {% endfor %}
{% else %}
<p class="empty-state">Featured publications will appear here.</p>
{% endif %}
</div>

<p>For a full list, see my <a href="{{ site.author.googlescholar }}">Google Scholar</a> or the <a href="{{ '/publications/' | relative_url }}">full publications page</a>.</p>

<h1 id="blog">Selected Blogs</h1>

{% assign featured_posts = site.posts | where: "featured", true %}
{% if featured_posts.size > 0 %}
  {% for post in featured_posts %}
<div class="pub-card">
  {% if post.thumbnail %}
  <img class="pub-thumb" src="{{ post.thumbnail | relative_url }}" alt="{{ post.title | strip_html }}" onerror="this.style.display='none'"/>
  {% endif %}
  <div class="pub-body">
    <h4><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
    {% if post.excerpt %}<p class="pub-excerpt">{{ post.excerpt | strip_html | truncatewords: 30 }}</p>{% endif %}
    <p class="pub-venue">
      {{ post.date | date: "%B %Y" }} &nbsp; <a href="{{ post.url | relative_url }}">Read &rarr;</a>
    </p>
  </div>
</div>
<hr class="pub-sep"/>
  {% endfor %}
{% else %}
<p class="empty-state">Blog posts coming soon.</p>
{% endif %}

<h1 id="cv">Curriculum Vitae</h1>

<p><a href="{{ '/files/Resume.pdf' | relative_url }}" class="btn btn--inverse">Download CV (PDF)</a></p>

<h1 id="contact">Get in touch</h1>

<p>
  Email: <a href="mailto:{{ site.author.email }}">{{ site.author.email }}</a><br/>
  <a href="https://github.com/{{ site.author.github }}">GitHub</a> &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/{{ site.author.linkedin }}">LinkedIn</a> &nbsp;·&nbsp;
  <a href="https://twitter.com/{{ site.author.twitter }}">Twitter</a> &nbsp;·&nbsp;
  <a href="{{ site.author.googlescholar }}">Google Scholar</a>
</p>
