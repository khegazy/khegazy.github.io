---
title: "Welcome to the Blog (Gibberish Edition)"
date: 2026-04-18
permalink: /posts/2026/04/welcome-to-the-blog/
header:
  teaser: "500x300.png"
excerpt: "A short lorem-ipsum note standing in for a real welcome post — meant only to exercise the theme's typography, MathJax, and the collapsible derivation component."
categories:
  - meta
tags:
  - placeholder
  - lorem-ipsum
  - test
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit. This is a
short placeholder post whose only job is to show what the blog index
looks like with real entries in `_posts/`. Delete it whenever.

The site renders math via MathJax, and the kramdown-safe convention
is to use `$$...$$` for *both* inline and display math — kramdown
decides which based on whether blank lines surround the expression.
So inline-wise, the ipsum loss $$\mathcal{L}(\theta)$$ shows up mid
sentence, while the same expression on its own block

$$
\mathcal{L}(\theta)
= \mathbb{E}_{x \sim p}\!\bigl[\ell(f_\theta(x),\,y)\bigr]
$$

renders as a display equation. Curabitur pretium tincidunt lacus.

Clicking the toggle below is how the more technical posts will hide
long derivations by default:

<details class="derivation" markdown="1">
<summary>Show the "derivation" (gibberish)</summary>

Starting from absolutely nothing and applying the well-known
*lemma of lorem*:

$$
\begin{aligned}
\mathcal{L}(\theta)
&= \int \ell(f_\theta(x), y)\, p(x, y)\, \mathrm{d}x\, \mathrm{d}y \\
&= \int \ell(f_\theta(x), y)\, p(y \mid x)\, p(x)\, \mathrm{d}x\, \mathrm{d}y \\
&\stackrel{\text{(ipsum)}}{=} \mathbb{E}_{x \sim p}\!\bigl[\mathbb{E}_{y \mid x}[\ell(f_\theta(x), y)]\bigr].
\end{aligned}
$$

which is the promised result. $\blacksquare$ (Fake QED. Nothing was
actually derived.)

</details>

Donec vitae sapien ut libero venenatis faucibus. This post, like the
other two, is a placeholder.
