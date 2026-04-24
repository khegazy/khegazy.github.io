---
permalink: /
title: "Kareem Hegazy"
excerpt: "Postdoctoral researcher at UC Berkeley / Berkeley Lab / ICSI. Physics PhD from Stanford."
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<style>
/* Homepage section tweaks */
.page__content h1,
.page__content h2 {
  margin-top: 2.25em;
  padding-bottom: 0.25em;
  border-bottom: 1px solid #eee;
}
.page__content h1:first-of-type { margin-top: 1em; }

/* Clickable publication card (title / authors / venue) */
.pub-link-card {
  display: block;
  text-decoration: none !important;
  color: inherit;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  padding: 0.9rem 1.15rem;
  margin: 0.7rem 0;
  transition: background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}
.pub-link-card:hover {
  background: #fafafa;
  border-color: #c9c9c9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  text-decoration: none;
}
.pub-link-card h4 {
  margin: 0 0 0.3em 0;
  font-weight: 600;
  color: #222;
}
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

/* Blog card (still uses thumbnail layout) */
.pub-card {
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
  margin: 1.25rem 0;
}
.pub-card .pub-thumb {
  width: 180px;
  max-width: 30%;
  flex-shrink: 0;
  border-radius: 4px;
}
.pub-card .pub-body { flex: 1; min-width: 0; }
.pub-card h4 { margin: 0 0 0.35em 0; font-weight: 600; }
.pub-card .pub-excerpt { color: #444; font-style: italic; margin: 0.25em 0 0.5em 0; }
.pub-card .pub-venue { margin: 0.15em 0; font-size: 0.95em; color: #555; }

.empty-state {
  color: #777;
  font-style: italic;
  padding: 0.75rem 0;
}

@media (max-width: 600px) {
  .pub-card { flex-direction: column; }
  .pub-card .pub-thumb { width: 100%; max-width: 100%; }
}
</style>

I am a postdoctoral researcher at [UC Berkeley](https://statistics.berkeley.edu/), [Lawrence Berkeley National Lab](https://www.lbl.gov/), and [ICSI](https://www.icsi.berkeley.edu/icsi/), working with [Michael Mahoney](https://www.stat.berkeley.edu/~mmahoney/) and [Benjamin Erichson](https://www.benerichson.com/) at the intersection of Physics, Chemistry, and AI. I received my Physics PhD from Stanford in 2023 under [Phil Bucksbaum](https://physics.stanford.edu/people/philip-bucksbaum) and [Ryan Coffee](https://profiles.stanford.edu/ryan-coffee), where I studied excited-state quantum molecular dynamics through [ultrafast gas-phase diffraction](https://lcls.slac.stanford.edu/instruments/mev-ued). In summer 2019 I was an AI Research Fellow at Google X on the [Blueshift team](https://research.google/teams/blueshift/). I previously earned an Honors B.Sc. in Physics and Math from the University of Michigan, where I researched the Higgs Boson at CERN with [Bing Zhou](https://lsa.umich.edu/physics/people/faculty/bzhou.html).

I am broadly interested in the intersection of physics and machine learning — LLMs for time series, ML for thermodynamic processes and PDE modeling, ML chemical potentials, and inverse problems.

<h1 id="publications">Selected Publications</h1>

{% assign featured_pubs = site.publications | where: "featured", true | sort: "date" | reverse %}
{% if featured_pubs.size > 0 %}
  {% for pub in featured_pubs %}
    {% if pub.paperurl and pub.paperurl != "" %}
      {% assign pub_href = pub.paperurl %}
    {% else %}
      {% assign pub_href = pub.permalink | relative_url %}
    {% endif %}
<a class="pub-link-card" href="{{ pub_href }}">
  <h4>{{ pub.title }}</h4>
  {% if pub.authors %}<p class="pub-authors">{{ pub.authors }}</p>{% endif %}
  <p class="pub-venue">{{ pub.venue }}{% if pub.date %}, {{ pub.date | date: "%Y" }}{% endif %}</p>
</a>
  {% endfor %}
{% else %}
<p class="empty-state">Featured publications will appear here.</p>
{% endif %}

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
