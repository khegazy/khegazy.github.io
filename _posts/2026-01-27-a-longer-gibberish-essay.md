---
title: "A Longer Gibberish Essay: Ipsum Flows on Lorem Manifolds"
date: 2026-01-27
permalink: /posts/2026/01/longer-essay/
header:
  teaser: "500x300.png"
excerpt: "Longer placeholder essay that stress-tests the theme on a multi-screen technical post: display math, aligned derivations, several collapsible proof-sketches, and a closing table."
categories:
  - essays
tags:
  - placeholder
  - long-form
  - lorem-ipsum
  - math
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit. This
fictional essay pretends to introduce *ipsum flows on lorem
manifolds* — a nonexistent object — so that the longer-form
technical-writing look and feel of the blog can be evaluated:
headings, paragraphs, display math, and several collapsible
derivation panels.

## 1. Setting and notation

Let $$(\mathcal{M}, g)$$ be a (fake) Riemannian manifold with
metric tensor $$g$$, and let $$\pi \in \mathcal{P}(\mathcal{M})$$ be
a probability measure on it. Denote by $$\nabla^g$$ the Levi-Civita
connection and by $$\mathrm{div}_g$$ the metric divergence. A *lorem
flow* is a family $$(\rho_t)_{t \ge 0} \subset \mathcal{P}(\mathcal{M})$$
satisfying the continuity-style equation

$$
\partial_t \rho_t + \mathrm{div}_g\!\bigl(\rho_t\, v_t\bigr) \;=\; 0,
\qquad v_t := -\nabla^g \frac{\delta \mathcal{F}}{\delta \rho}(\rho_t),
\label{eq:lorem-flow}
$$

for some (fake) energy functional $$\mathcal{F}: \mathcal{P}(\mathcal{M}) \to \mathbb{R}$$.
If $$\mathcal{F}$$ were the KL divergence to a fixed target, this
would be the gradient flow of relative entropy — but here it is
nothing, because the whole setup is gibberish.

## 2. A "key identity"

The following identity drives most of what follows. Its one-line
statement:

$$
\frac{\mathrm{d}}{\mathrm{d}t} \mathcal{F}(\rho_t)
\;=\; -\int_{\mathcal{M}} \bigl\lVert \nabla^g \tfrac{\delta \mathcal{F}}{\delta \rho}(\rho_t) \bigr\rVert_g^2\, \rho_t\, \mathrm{d}\mathrm{vol}_g.
\label{eq:dissipation}
$$

Readers who want only the headline can skip the derivation.

<details class="derivation" markdown="1">
<summary>Derivation of the "energy dissipation" identity</summary>

Differentiating $$\mathcal{F}(\rho_t)$$ and applying the chain rule
in $$\mathcal{P}(\mathcal{M})$$:

$$
\begin{aligned}
\frac{\mathrm{d}}{\mathrm{d}t} \mathcal{F}(\rho_t)
&= \int_{\mathcal{M}} \tfrac{\delta \mathcal{F}}{\delta \rho}(\rho_t)\, \partial_t \rho_t\, \mathrm{d}\mathrm{vol}_g \\
&\stackrel{\eqref{eq:lorem-flow}}{=} -\int_{\mathcal{M}} \tfrac{\delta \mathcal{F}}{\delta \rho}(\rho_t)\, \mathrm{div}_g\!\bigl(\rho_t\, v_t\bigr)\, \mathrm{d}\mathrm{vol}_g \\
&\stackrel{\text{(IBP)}}{=} \int_{\mathcal{M}} \bigl\langle \nabla^g \tfrac{\delta \mathcal{F}}{\delta \rho}(\rho_t),\, v_t \bigr\rangle_g\, \rho_t\, \mathrm{d}\mathrm{vol}_g \\
&\stackrel{(v_t = -\nabla^g \tfrac{\delta \mathcal{F}}{\delta \rho})}{=}
-\int_{\mathcal{M}} \bigl\lVert \nabla^g \tfrac{\delta \mathcal{F}}{\delta \rho}(\rho_t) \bigr\rVert_g^2\, \rho_t\, \mathrm{d}\mathrm{vol}_g.
\end{aligned}
$$

Integration by parts requires the obvious (fake) boundary /
decay conditions. $\blacksquare$

</details>

The sign of \eqref{eq:dissipation} is the only substantive content:
$$\mathcal{F}$$ is non-increasing along the flow. Donec placerat,
nibh ac aliquam mattis, ligula nisi porta justo.

## 3. Discretization

A plausible-looking numerical scheme for \eqref{eq:lorem-flow} is
the (totally invented) *implicit ipsum step*:

$$
\rho_{k+1} \;\in\; \arg\min_{\rho \in \mathcal{P}(\mathcal{M})}\;
\Bigl\{\, \mathcal{F}(\rho) \;+\; \tfrac{1}{2\tau}\, W_2^2(\rho, \rho_k) \,\Bigr\},
$$

where $$W_2$$ is the 2-Wasserstein distance and $$\tau > 0$$ is a
step size. For Euclidean $$\mathcal{M}$$ and quadratic
$$\mathcal{F}$$ this has a closed-form update; in general it does
not.

<details class="derivation" markdown="1">
<summary>Show the closed-form update for quadratic $$\mathcal{F}$$</summary>

Take $$\mathcal{M} = \mathbb{R}^d$$ and
$$\mathcal{F}(\rho) = \tfrac{1}{2}\,\mathbb{E}_{X \sim \rho}\bigl[\lVert X - \mu \rVert^2\bigr]$$
for some fixed $$\mu \in \mathbb{R}^d$$. Using the fact that
$$W_2^2$$ factorizes on means + covariances for Gaussian-like
measures (we assume $$\rho_k$$ is Gaussian without loss of
generality — this is also fake),

$$
\begin{aligned}
\mu_{k+1}
&= \arg\min_m\; \tfrac{1}{2}\,\lVert m - \mu \rVert^2 + \tfrac{1}{2\tau}\,\lVert m - \mu_k \rVert^2 \\
&= \frac{\tau\, \mu + \mu_k}{\tau + 1}
\;=\; \mu_k + \frac{\tau}{1 + \tau}\,(\mu - \mu_k).
\end{aligned}
$$

i.e., an implicit gradient step with rate
$$\tau / (1 + \tau)$$ — which, for small $$\tau$$, recovers the
explicit flow as expected.

</details>

## 4. Consequences (none)

Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.
The two identities above are, in the real literature, genuinely
true statements about gradient flows in Wasserstein space — see
Jordan–Kinderlehrer–Otto (1998), Ambrosio–Gigli–Savaré (2008), and
Otto (2001) for actual references. Nothing specific to this post is
real.

### 4.1 A list of fake consequences

1. Ipsum entropy is monotone, therefore *everything is fine*.
2. Lorem manifolds are geodesically convex (not checked).
3. Consectetur $$\ge 0$$ for integrable elits (undefined).
4. The scheme converges at rate $$\mathcal{O}(\tau)$$, obviously.

### 4.2 A pair of unordered nonsense

- Adipiscing incididunt, except when it does.
- Ut labore sed do eiusmod tempor.
- Excepteur sint occaecat cupidatat non proident.

## 5. Where to go from here

<details class="aside" markdown="1">
<summary>Aside: connection to ipsum-regularized transport</summary>

If one adds an entropic penalty $$\varepsilon H(\rho)$$ to
$$\mathcal{F}$$, the flow becomes a noisy SDE of Fokker–Planck type
with diffusion $$\varepsilon$$. None of that matters here; this
aside exists only to show the lighter "aside" variant of the
toggle component.

</details>

Curabitur pretium tincidunt lacus. Nulla gravida orci a odio.
End of placeholder.
