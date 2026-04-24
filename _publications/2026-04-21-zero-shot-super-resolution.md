---
title: "The False Promise of Zero-Shot Super-Resolution in Machine-Learned Operators"
collection: publications
permalink: /publication/2026-04-21-zero-shot-super-resolution
featured: true
thumbnail: /images/publications/zero-shot-sr.png
excerpt: "Machine-learned operators cannot actually do zero-shot super-resolution — they're brittle and susceptible to aliasing off the training grid. A simple, data-driven multi-resolution training protocol restores accurate cross-resolution inference."
date: 2026-04-21
venue: "<i>ICLR</i> 2026"
journal: "ICLR 2026"
authors: "M. Sakarvadia, K. Hegazy, et al."
citation: "M. Sakarvadia, K. Hegazy, et al. (2026). &quot;The False Promise of Zero-Shot Super-Resolution in Machine-Learned Operators.&quot; <i>ICLR</i>."
paperurl: "https://openreview.net/forum?id=hkF7ZM7fEp&referrer=%5Bthe%20profile%20of%20Kareem%20Hegazy%5D(%2Fprofile%3Fid%3D~Kareem_Hegazy1)"
arxivurl: "https://arxiv.org/abs/2510.06646"
codeurl: ""
blogurl: "https://mansisak.com/operator_aliasing/"
---
An empirical critique of "zero-shot super-resolution" in machine-learned operators (MLOs) for PDEs, and a practical fix.

- Decomposes multi-resolution inference into two behaviors — frequency extrapolation and cross-resolution interpolation — and shows MLOs fail at both in a zero-shot setting.
- MLOs are brittle and susceptible to aliasing when evaluated at resolutions different from their training grid, both for super- and sub-resolution.
- Proposes a simple, computationally-efficient, data-driven multi-resolution training protocol that overcomes aliasing and restores robust multi-resolution generalization.
