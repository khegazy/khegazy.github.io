"""
Behavioral tests for khegazy.github.io.

These tests verify the site contents without needing a full Jekyll build.
They check:
  - YAML front matter on all publication files
  - The "featured publications" filter + sort used on the homepage
    produces the expected, date-descending ordering
  - Liquid tag balance in templates we edit
  - Navigation URLs resolve to real pages/files in the repo
  - Masthead has the 5 expected social icons and the nav-start pivot
  - About.md contains required sections and does NOT contain removed
    dissertation content
  - _config.yml author fields are populated
  - Every {{ site.author.X }} used in templates resolves to a non-empty value
  - Internal links in about.html (e.g., /files/Resume.pdf) point to files
    that exist in the repo

Run:  python3 tests/site_tests.py
"""

from __future__ import annotations

import os
import re
import sys
import unittest
from pathlib import Path
from datetime import date

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    print("PyYAML is required. Install with: pip install pyyaml --break-system-packages")
    sys.exit(2)


REPO = Path(__file__).resolve().parent.parent
PUBS_DIR = REPO / "_publications"
POSTS_DIR = REPO / "_posts"
PAGES_DIR = REPO / "_pages"
INCLUDES_DIR = REPO / "_includes"
DATA_DIR = REPO / "_data"
FILES_DIR = REPO / "files"


# ---------- helpers ----------

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_front_matter(path: Path):
    """Return (meta_dict, body_str)."""
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        raise AssertionError(f"{path}: missing YAML front matter")
    meta = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    return meta, body


def load_config():
    return yaml.safe_load((REPO / "_config.yml").read_text(encoding="utf-8"))


def load_navigation():
    return yaml.safe_load((DATA_DIR / "navigation.yml").read_text(encoding="utf-8"))


def count_liquid_tags(s: str):
    """Return (opens, closes) for balance-only structural tags that need
    explicit closes: if/for/unless/capture/assign-is-self-closing.
    We count opening/closing tags of the major block constructs."""
    opens = 0
    closes = 0
    for m in re.finditer(r"\{%-?\s*(\w+)\b", s):
        tag = m.group(1)
        if tag in ("if", "for", "unless", "capture"):
            opens += 1
        elif tag in ("endif", "endfor", "endunless", "endcapture"):
            closes += 1
    return opens, closes


# ---------- tests ----------

class PublicationFrontMatterTests(unittest.TestCase):
    REQUIRED = ("title", "collection", "permalink", "date", "venue", "authors")

    def setUp(self):
        self.files = sorted(PUBS_DIR.glob("*.md"))

    def test_exactly_six_publications(self):
        names = [p.name for p in self.files]
        self.assertEqual(
            len(self.files), 6,
            f"Expected 6 publication files, got {len(self.files)}: {names}"
        )

    def test_no_academicpages_placeholders_remain(self):
        names = {p.name for p in self.files}
        placeholders = {
            "2009-10-01-paper-title-number-1.md",
            "2010-10-01-paper-title-number-2.md",
            "2015-10-01-paper-title-number-3.md",
        }
        leftover = names & placeholders
        self.assertFalse(leftover, f"Placeholder files still present: {leftover}")

    def test_each_pub_has_required_fields(self):
        for p in self.files:
            with self.subTest(file=p.name):
                meta, _body = parse_front_matter(p)
                for key in self.REQUIRED:
                    self.assertIn(key, meta, f"{p.name}: missing '{key}'")
                    self.assertTrue(
                        str(meta[key]).strip(),
                        f"{p.name}: '{key}' is empty",
                    )
                self.assertEqual(
                    meta["collection"], "publications",
                    f"{p.name}: collection must be 'publications'",
                )
                self.assertIsInstance(
                    meta["date"], date,
                    f"{p.name}: 'date' must parse to a date, got {type(meta['date']).__name__}",
                )

    def test_all_six_are_featured(self):
        for p in self.files:
            with self.subTest(file=p.name):
                meta, _ = parse_front_matter(p)
                self.assertTrue(
                    meta.get("featured") is True,
                    f"{p.name}: 'featured' should be True (is {meta.get('featured')!r})",
                )

    def test_permalink_matches_permalink_convention(self):
        # collections use /:collection/:path/ — so permalink should start with /publication/
        for p in self.files:
            with self.subTest(file=p.name):
                meta, _ = parse_front_matter(p)
                self.assertTrue(
                    meta["permalink"].startswith("/publication/"),
                    f"{p.name}: permalink should start with /publication/, got {meta['permalink']!r}",
                )


class FeaturedSortOrderTests(unittest.TestCase):
    """Replicate Liquid: site.publications | where: featured | sort: date | reverse"""

    EXPECTED_ORDER = [
        "2026-06-01-neurde.md",
        "2026-05-01-powerformer.md",
        "2026-04-21-zero-shot-super-resolution.md",
        "2025-10-01-popcornn.md",
        "2024-09-01-nitrobenzene-dissociation.md",
        "2023-10-01-bayesian-inference-gas-diffraction.md",
    ]

    def test_featured_desc_by_date(self):
        pubs = []
        for p in sorted(PUBS_DIR.glob("*.md")):
            meta, _ = parse_front_matter(p)
            if meta.get("featured") is True:
                pubs.append((meta["date"], p.name))
        pubs.sort(key=lambda x: x[0], reverse=True)
        actual = [name for _, name in pubs]
        self.assertEqual(actual, self.EXPECTED_ORDER,
                         f"Featured order mismatch.\nExpected: {self.EXPECTED_ORDER}\nActual:   {actual}")


class LiquidBalanceTests(unittest.TestCase):
    def test_about_md_tag_balance(self):
        text = (PAGES_DIR / "about.html").read_text(encoding="utf-8")
        o, c = count_liquid_tags(text)
        self.assertEqual(o, c, f"about.html has unbalanced Liquid tags: {o} opens vs {c} closes")

    def test_masthead_tag_balance(self):
        text = (INCLUDES_DIR / "masthead.html").read_text(encoding="utf-8")
        o, c = count_liquid_tags(text)
        self.assertEqual(o, c, f"masthead.html has unbalanced Liquid tags: {o} opens vs {c} closes")


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.nav = load_navigation()
        self.main = self.nav.get("main", [])

    def test_nav_has_all_expected_items(self):
        titles = [item["title"] for item in self.main]
        self.assertEqual(titles, ["Home", "Publications", "Blog", "CV", "Contact"])

    def test_nav_urls_resolve(self):
        # URL -> what we expect to exist in the repo. Homepage-anchor URLs
        # (e.g. "/#publications", "/#contact") are validated by looking
        # up the matching id= on about.html.
        checks = {
            "/": PAGES_DIR / "about.html",
            "/year-archive/": PAGES_DIR / "year-archive.html",
            "/files/Resume.pdf": FILES_DIR / "Resume.pdf",
        }
        about_text = (PAGES_DIR / "about.html").read_text(encoding="utf-8")
        for item in self.main:
            url = item["url"]
            if url.startswith("/#"):
                anchor = url[2:]  # strip leading "/#"
                self.assertIn(
                    f'id="{anchor}"', about_text,
                    f"Nav '{item['title']}' points to {url}, but about.html "
                    f"has no matching id=\"{anchor}\" to scroll to",
                )
                continue
            target = checks.get(url)
            self.assertIsNotNone(target, f"Unexpected nav URL: {url}")
            self.assertTrue(target.exists(),
                            f"Nav '{item['title']}' points to {url}, but {target} does not exist")

    def test_publications_nav_anchors_home_section(self):
        # User wants the Publications nav link to scroll to the Selected
        # Publications block on the homepage (not navigate away to the
        # full archive page).
        urls = {item["url"] for item in self.main}
        self.assertIn(
            "/#publications", urls,
            "Publications nav link should be '/#publications' so it "
            "scrolls to the Selected Publications section on the homepage",
        )


class MastheadTests(unittest.TestCase):
    def setUp(self):
        self.text = (INCLUDES_DIR / "masthead.html").read_text(encoding="utf-8")

    def test_has_each_social_icon(self):
        for needle in (
            "site.author.github",
            "site.author.linkedin",
            "site.author.twitter",
            "site.author.googlescholar",
            "site.author.email",
        ):
            with self.subTest(field=needle):
                self.assertIn(needle, self.text,
                              f"masthead.html missing reference to {needle}")

    def test_uses_flex_layout_for_nav(self):
        # We use flex (not the spacer-cell table hack) so nav items stay
        # visible. A helper JS block neutralizes greedy-nav's overflow JS.
        self.assertRegex(
            self.text,
            r"\.visible-links\s*\{[^}]*display:\s*flex",
            "masthead.html should use display: flex on .visible-links",
        )

    def test_first_nav_item_pushed_right(self):
        # margin-left: auto on the FIRST nav <li> pushes every remaining
        # nav item to the right side of the bar, after the social icons.
        # CSS has no ":first-of-class", so we use the adjacent-sibling
        # combinator: a --nav <li> that directly follows a --social <li>
        # is exactly the first nav item (only one such pair exists).
        #
        # Regression guard: :first-of-type does NOT work here because
        # every child of .visible-links is an <li>, so :first-of-type
        # matches the first li in the list (a social icon), not the
        # first --nav li.
        self.assertNotRegex(
            self.text,
            r"\.masthead__menu-item--nav:first-of-type\s*\{",
            "masthead.html must NOT use :first-of-type to select the first "
            "nav <li> — every child is an <li>, so it matches the first "
            "SOCIAL icon instead of the first nav item",
        )
        self.assertRegex(
            self.text,
            r"\.masthead__menu-item--social\s*\+\s*\.masthead__menu-item--nav\s*\{[^}]*margin-left:\s*auto",
            "masthead.html should push nav items right via the adjacent-"
            "sibling selector '.masthead__menu-item--social + "
            ".masthead__menu-item--nav { margin-left: auto }'",
        )

    def test_no_spacer_cell(self):
        # The spacer <li> broke greedy-nav's overflow detection by making
        # .visible-links always full-width. Flex layout replaces it.
        self.assertNotIn("masthead__menu-item--spacer", self.text,
                         "masthead.html should no longer include the spacer "
                         "<li> — it caused greedy-nav to shove items into the "
                         "hamburger. Flex + margin-left: auto is the fix.")

    def test_greedy_nav_is_neutralized(self):
        # A short JS block overrides window.updateNav to no-op so the theme
        # doesn't move nav items into the hamburger dropdown.
        self.assertIn("window.updateNav", self.text,
                      "masthead.html should override window.updateNav to disable "
                      "the theme's greedy-nav overflow logic")
        self.assertIn("hidden-links", self.text,
                      "masthead.html neutralizer should move .hidden-links items "
                      "back into .visible-links if the theme already shuffled them")

    def test_hamburger_button_removed(self):
        # The theme's greedy-nav JS relies on $btn.width() to compute
        # available space. With no <button>, the expression resolves to
        # NaN — all its comparisons become false and it stops trying to
        # move links into a hamburger dropdown. That is how we guarantee
        # the social icons and nav links stay visible.
        self.assertNotRegex(
            self.text,
            r'<button\b[^>]*>\s*<div class="navicon"',
            "masthead.html should NOT include the greedy-nav hamburger "
            "<button> — its presence makes the theme JS move links into "
            "a dropdown. Removing it short-circuits the overflow logic.",
        )

    def test_iterates_navigation_data(self):
        self.assertIn("site.data.navigation.main", self.text,
                      "masthead.html should iterate site.data.navigation.main")

    def test_masthead_is_sticky(self):
        # The masthead should pin to the top as the page scrolls
        # (both the vendor-prefixed and bare form count as sticky).
        self.assertRegex(
            self.text,
            r"\.masthead\s*\{[^}]*position:\s*(?:-webkit-)?sticky",
            "masthead.html should have position: sticky on .masthead",
        )
        self.assertRegex(
            self.text,
            r"\.masthead\s*\{[^}]*top:\s*0",
            "masthead.html sticky .masthead should set top: 0",
        )

    def test_scroll_progress_bar_present(self):
        # The #scroll-progress element lives inside the sticky masthead so
        # it sits on top of the nav's border and sticks with it.
        self.assertIn('id="scroll-progress"', self.text,
                      "masthead.html should include the #scroll-progress bar element")
        self.assertRegex(
            self.text,
            r"#scroll-progress\s*\{[^}]*position:\s*absolute",
            "masthead.html #scroll-progress should be position: absolute",
        )
        self.assertRegex(
            self.text,
            r"#scroll-progress\s*\{[^}]*height:\s*\d",
            "masthead.html #scroll-progress should declare a height",
        )

    def test_scroll_progress_has_update_script(self):
        # The progress bar needs a scroll listener that updates its width.
        self.assertIn("scroll-progress", self.text)
        self.assertIn("addEventListener('scroll'", self.text,
                      "masthead.html should attach a scroll listener for the progress bar")
        self.assertIn("requestAnimationFrame", self.text,
                      "masthead.html scroll listener should be rAF-debounced")


class AboutPageTests(unittest.TestCase):
    def setUp(self):
        self.text = (PAGES_DIR / "about.html").read_text(encoding="utf-8")
        self.meta, self.body = parse_front_matter(PAGES_DIR / "about.html")

    def test_permalink_is_root(self):
        self.assertEqual(self.meta.get("permalink"), "/",
                         "about.html permalink should be '/'")

    def test_author_profile_disabled(self):
        # The homepage was redesigned: the bio + photo now live inline in a
        # scrolling hero section (not a sticky sidebar). The sidebar should
        # therefore be OFF on the homepage.
        self.assertFalse(
            self.meta.get("author_profile"),
            "about.html should have author_profile: false — the homepage uses "
            "an inline hero section instead of the sticky author sidebar",
        )

    def test_wide_page_class_set(self):
        # With the sidebar off, the content area should stretch to full width.
        classes = self.meta.get("classes")
        if isinstance(classes, list):
            self.assertIn("wide-page", classes,
                          "about.html should include 'wide-page' in classes: list")
        else:
            self.assertEqual(classes, "wide-page",
                             "about.html classes: should be 'wide-page' (full-width layout)")

    def test_hero_section_present(self):
        self.assertRegex(
            self.body,
            r'<section\s+class="hero"',
            "about.html should have a <section class='hero'> containing bio + photo",
        )

    def test_hero_image_references_profile(self):
        self.assertRegex(
            self.body,
            r'<img\s+class="hero__image"[^>]*profile\.png',
            "about.html hero should include an <img class='hero__image'> pointing at profile.png",
        )

    def test_hero_image_precedes_hero_text(self):
        # The user wants the photo on the LEFT of the bio.
        # In a horizontal flex row, that means the <img> must come before
        # the .hero__text <div> in source order.
        img_idx = self.body.find('class="hero__image"')
        text_idx = self.body.find('class="hero__text"')
        self.assertNotEqual(img_idx, -1, "hero__image missing")
        self.assertNotEqual(text_idx, -1, "hero__text missing")
        self.assertLess(
            img_idx, text_idx,
            "hero__image must appear before hero__text in source order so the "
            "photo renders on the LEFT of the bio (flex row).",
        )

    def test_hero_mobile_stacks_without_reversing(self):
        # On narrow viewports the flex direction should be 'column' (image
        # on top, bio below) — NOT 'column-reverse', which flips the user's
        # requested image-on-top ordering.
        self.assertNotRegex(
            self.body,
            r"flex-direction:\s*column-reverse",
            "about.html @media block must use flex-direction: column "
            "(not column-reverse) so the photo stays above the bio on mobile",
        )

    def test_page_title_is_hidden_on_homepage(self):
        # The theme's single.html renders <h1 class="page__title"> from the
        # front matter title, which duplicated the hero name. Hide it on
        # the homepage.
        self.assertRegex(
            self.body,
            r"\.page__title\s*\{[^}]*display:\s*none",
            "about.html should hide the theme's duplicate .page__title heading",
        )

    def test_content_area_widened_on_homepage(self):
        # The theme's .page uses span(10 of 12) with suffix(2 of 12),
        # leaving a large empty right gutter even with no sidebar. The
        # homepage override should reset .page + .page__inner-wrap +
        # .page__content to full width / no margin / no padding so every
        # child of .page__content (hero, h1, pub cards, contact block)
        # shares the same left/right edges.
        # The selector list now also targets .home and its direct children
        # as a defense-in-depth against Susy gutters leaking through any
        # inner wrapper — but .page, .page__inner-wrap, .page__content
        # must be the FIRST three selectors so the core wrappers are
        # guaranteed to be reset.
        self.assertRegex(
            self.body,
            r"\.page,\s*\.page__inner-wrap,\s*\.page__content\b",
            "about.html should list .page, .page__inner-wrap, and "
            ".page__content together in the width/margin/padding override",
        )
        self.assertRegex(
            self.body,
            r"\.page,[^{]*\{[^}]*width:\s*100%",
            "about.html .page override should set width: 100%",
        )
        self.assertRegex(
            self.body,
            r"\.page,[^{]*\{[^}]*float:\s*none",
            "about.html .page override should also reset float: none",
        )

    def test_main_centered_with_consistent_padding(self):
        # #main needs explicit auto left/right margins so the max-width
        # cap renders as an even gutter on both sides of the page.
        self.assertRegex(
            self.body,
            r"#main\s*\{[^}]*margin-left:\s*auto",
            "about.html #main override should set margin-left: auto so the "
            "capped content is horizontally centered",
        )
        self.assertRegex(
            self.body,
            r"#main\s*\{[^}]*margin-right:\s*auto",
            "about.html #main override should set margin-right: auto",
        )

    def test_hero_image_is_rectangular(self):
        # User wants the full rectangular profile.png, not a circular crop.
        # Guard against reintroducing border-radius: 50% or object-fit: cover.
        self.assertNotRegex(
            self.body,
            r"\.hero__image\s*\{[^}]*border-radius:\s*50%",
            "about.html .hero__image should NOT use border-radius: 50% — "
            "the user wants the full rectangular image, not a circular crop",
        )
        self.assertNotRegex(
            self.body,
            r"\.hero__image\s*\{[^}]*object-fit:\s*cover",
            "about.html .hero__image should NOT use object-fit: cover — "
            "the user wants the full rectangular image without cropping",
        )

    def test_publications_anchor_exists(self):
        # The Publications nav link scrolls to /#publications, so the
        # homepage must define id="publications" for the browser to
        # find its scroll target.
        self.assertIn(
            'id="publications"', self.body,
            "about.html should define id=\"publications\" (the nav link "
            "'/#publications' scrolls to it)",
        )

    def test_scholar_callout_after_pubs(self):
        # User wants a callout line at the end of the selected publications
        # with the text pointing to their Scholar page and a matching
        # graduation-cap icon button (same icon used in the masthead).
        self.assertIn(
            "scholar-callout", self.body,
            "about.html should include a .scholar-callout block after the "
            "Selected Publications list",
        )
        self.assertIn(
            "scholar page for all my up-to-date publications", self.body,
            "about.html scholar-callout should carry the user's requested "
            "copy (\"scholar page for all my up-to-date publications\")",
        )
        # The button must use the same Font Awesome graduation-cap icon
        # as the masthead's Google Scholar social icon, and link to
        # site.author.googlescholar.
        self.assertRegex(
            self.body,
            r'class="scholar-callout__link"[^>]*href="\{\{\s*site\.author\.googlescholar\s*\}\}"',
            "about.html scholar-callout link should use "
            "href=\"{{ site.author.googlescholar }}\" (same as masthead)",
        )
        self.assertRegex(
            self.body,
            r'scholar-callout__link[^<]*<i[^>]*fa-graduation-cap',
            "about.html scholar-callout should render the fa-graduation-cap "
            "icon (the same one used in the masthead)",
        )

    def test_scholar_callout_flex_layout(self):
        # Text on the left, button on the right — flex with
        # justify-content: space-between is how we position them.
        self.assertRegex(
            self.body,
            r"\.scholar-callout\s*\{[^}]*display:\s*flex",
            "about.html .scholar-callout should use display: flex",
        )
        self.assertRegex(
            self.body,
            r"\.scholar-callout\s*\{[^}]*justify-content:\s*space-between",
            "about.html .scholar-callout should use justify-content: "
            "space-between so the button sits on the right",
        )

    def test_hero_is_vertically_centered(self):
        # The user wants the photo vertically centered with the bio, not
        # anchored to the top of the text column.
        self.assertRegex(
            self.body,
            r"\.hero\s*\{[^}]*align-items:\s*center",
            "about.html .hero should use align-items: center so the photo "
            "is vertically aligned with the midpoint of the bio text",
        )
        self.assertNotRegex(
            self.body,
            r"\.hero\s*\{[^}]*align-items:\s*flex-start",
            "about.html .hero should NOT use align-items: flex-start — that "
            "anchors the photo to the top of the text, which looks awkward",
        )

    def test_hero_has_name_and_subtitle(self):
        self.assertIn('class="hero__name"', self.body,
                      "about.html hero should render a .hero__name element")
        self.assertIn('class="hero__subtitle"', self.body,
                      "about.html hero should render a .hero__subtitle element (role/affiliations)")

    def test_hero_bio_contains_collaborator_links(self):
        # The page is now .html (not .md) so the bio uses explicit <a>
        # tags instead of markdown [text](url). Regression guard that the
        # key collaborator links are still present and well-formed.
        for needle in (
            'statistics.berkeley.edu',      # UC Berkeley
            'lbl.gov',                       # LBL
            'icsi.berkeley.edu',             # ICSI
            'mmahoney',                      # Michael Mahoney
            'benerichson.com',               # Ben Erichson
            'philip-bucksbaum',              # Phil Bucksbaum
            'ryan-coffee',                   # Ryan Coffee
        ):
            with self.subTest(link=needle):
                self.assertIn(needle, self.body,
                              f"about.html .hero__bio should include a link to {needle}")

    def test_required_sections(self):
        for heading in ("Selected Publications", "Selected Blogs",
                        "Curriculum Vitae", "Get in touch"):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.body,
                              f"about.html missing required section: {heading}")

    def test_no_dissertation_content(self):
        # User asked to remove dissertation-related content from the bio.
        self.assertNotRegex(self.body, r"(?i)\bdissertation\b",
                            "about.html still references 'dissertation' — the user asked to remove this")

    def test_featured_pub_liquid_loop(self):
        # Exact filter chain we committed: where featured true, sort date, reverse
        self.assertRegex(
            self.body,
            r'site\.publications\s*\|\s*where:\s*"featured",\s*true\s*\|\s*sort:\s*"date"\s*\|\s*reverse',
            "about.html is missing the featured-publications filter chain",
        )

    def test_featured_posts_liquid_loop(self):
        self.assertRegex(
            self.body,
            r'site\.posts\s*\|\s*where:\s*"featured",\s*true',
            "about.html is missing the featured-posts filter chain",
        )

    def test_pub_card_renders_excerpt(self):
        self.assertIn("pub.excerpt", self.body,
                      "homepage publication card should render pub.excerpt "
                      "(the description text that describes the paper)")

    def test_pub_card_uses_div_not_anchor_wrapper(self):
        # kramdown treats <a> as span-level, so wrapping <h4>/<p> in <a>
        # can mangle output. We use <div class="pub-link-card"> now and
        # put the <a> inside the title element.
        self.assertNotRegex(
            self.body,
            r'<a\s+class="pub-link-card"',
            "homepage publication card should NOT use <a class='pub-link-card'> "
            "as an outer wrapper (kramdown issue). Use <div> + stretched title link.",
        )
        self.assertRegex(
            self.body,
            r'<div\s+class="pub-link-card"',
            "homepage publication card should be a <div class='pub-link-card'>",
        )

    def test_pub_card_title_is_the_link(self):
        self.assertRegex(
            self.body,
            r'<h4\s+class="pub-title"><a\s+href="\{\{\s*pub_href\s*\}\}">',
            "the pub-title <h4> should wrap an <a> pointing at pub_href",
        )

    def test_pub_card_renders_action_buttons(self):
        # After the redesign, each pub card renders exactly three buttons
        # in this order:
        #   1. Journal — paperurl if published, gray disabled span if not
        #   2. Blog    — only if blogurl is set
        #   3. arXiv   — only if arxivurl is set
        # (Paper and Code buttons were removed; the journal name IS the
        # paper link.)
        self.assertRegex(
            self.body,
            r"pub-action--journal",
            "about.html pub cards should render a journal button "
            "(.pub-action--journal) as the primary action",
        )
        self.assertRegex(
            self.body,
            r"pub\.blogurl.*Blog",
            "about.html should still render the Blog button from pub.blogurl",
        )
        self.assertRegex(
            self.body,
            r"pub\.arxivurl.*arXiv",
            "about.html should still render the arXiv button from pub.arxivurl",
        )

    def test_pub_card_button_order_is_journal_blog_arxiv(self):
        # The user asked for the exact button order: Journal, then Blog,
        # then arXiv. Check on button-rendering tokens (the href=...
        # calls inside the actions block) rather than on pub.xxurl
        # references, since pub.arxivurl ALSO appears earlier in the
        # href-fallback chain and would pass the test incorrectly.
        journal_idx = self.body.find("pub-action--journal")
        blog_idx = self.body.find('href="{{ pub.blogurl }}"')
        arxiv_idx = self.body.find('href="{{ pub.arxivurl }}"')
        for name, idx in (
            ("journal", journal_idx),
            ("blog", blog_idx),
            ("arxiv", arxiv_idx),
        ):
            self.assertNotEqual(idx, -1, f"pub card template missing {name} button")
        self.assertLess(
            journal_idx, blog_idx,
            "Journal button should render before the Blog button in the pub card",
        )
        self.assertLess(
            blog_idx, arxiv_idx,
            "Blog button should render before the arXiv button in the pub card",
        )

    def test_pub_card_paper_and_code_buttons_removed(self):
        # The user's new design has no standalone "Paper" button (the
        # journal IS the paper link) and no "Code" button at all.
        self.assertNotRegex(
            self.body,
            r'>Paper<',
            "about.html pub cards should NOT render a standalone 'Paper' "
            "button — the journal button is the paper link",
        )
        self.assertNotRegex(
            self.body,
            r'>Code<',
            "about.html pub cards should NOT render a 'Code' button "
            "(removed in the simplified 3-button design)",
        )

    def test_pub_card_journal_disabled_when_no_paperurl(self):
        # Papers without a paperurl must render the journal button as a
        # disabled <span> (gray, unclickable) instead of an <a>.
        self.assertIn(
            "pub-action--disabled", self.body,
            "about.html should render unpublished papers' journal as "
            "<span class='pub-action--disabled'> (gray, not clickable)",
        )
        self.assertRegex(
            self.body,
            r'<span\s+class="pub-action\s+pub-action--journal\s+pub-action--disabled"',
            "the disabled journal button must be a <span>, not an <a>, "
            "so it cannot be clicked",
        )

    def test_pub_card_excerpt_renders_after_actions(self):
        # User requested excerpt on the BOTTOM of the card (below the
        # button row, not above it). Check source order.
        excerpt_idx = self.body.find("pub.excerpt")
        actions_idx = self.body.find('class="pub-actions"')
        self.assertNotEqual(excerpt_idx, -1, "pub card missing excerpt")
        self.assertNotEqual(actions_idx, -1, "pub card missing actions row")
        self.assertLess(
            actions_idx, excerpt_idx,
            "pub card actions row must render BEFORE the excerpt — "
            "the user wants the excerpt on the bottom of the card",
        )

    def test_pub_card_standalone_venue_line_removed(self):
        # The old "pub-venue" italic line under authors was replaced by
        # the journal button on publication cards. Check only the
        # pub-link-card block (blog cards use their own .pub-card with a
        # different .pub-venue for the date line — that's fine).
        pub_card_start = self.body.find('class="pub-link-card"')
        pub_card_end = self.body.find("</div>", pub_card_start)
        self.assertGreater(pub_card_start, -1, "pub-link-card block missing")
        pub_card_block = self.body[pub_card_start:pub_card_end]
        self.assertNotRegex(
            pub_card_block,
            r'<p\s+class="pub-venue"',
            "about.html pub-link-card should no longer render a standalone "
            "<p class='pub-venue'> line — the journal button replaces it",
        )

    def test_pub_action_buttons_above_stretched_link(self):
        # The .pub-actions container needs z-index higher than the stretched
        # title link's ::after (z-index: 1), or buttons become unclickable.
        self.assertRegex(
            self.body,
            r"\.pub-actions\s*\{[^}]*z-index:\s*2",
            "about.html .pub-actions must have z-index: 2 so buttons sit above "
            "the stretched title link overlay",
        )

    def test_pub_href_fallback_chain(self):
        # The card title's href should fall back:
        #   paperurl → arxivurl → permalink
        self.assertIn("pub.paperurl", self.body,
                      "about.html pub card link should prefer pub.paperurl")
        self.assertIn("pub.arxivurl", self.body,
                      "about.html pub card link should fall back to pub.arxivurl")
        self.assertIn("pub.permalink", self.body,
                      "about.html pub card link should ultimately fall back to pub.permalink")

    def test_no_auto_year_append_in_venue_line(self):
        # Earlier version appended ", {{ pub.date | date: '%Y' }}" to the
        # venue — awkward for "Under review at ICML, 2026". We now encode
        # year into the venue string itself.
        self.assertNotRegex(
            self.body,
            r'\{\{\s*pub\.venue\s*\}\}[^<]*\{\%\s*if\s+pub\.date',
            "about.html should not auto-append the year to the venue line",
        )

    def test_cv_download_link(self):
        self.assertIn("/files/Resume.pdf", self.body,
                      "about.html is missing the CV download link")

    def test_contact_email_uses_site_author(self):
        self.assertIn("{{ site.author.email }}", self.body,
                      "about.html contact should use {{ site.author.email }}")

    def test_contact_section_uses_icon_links(self):
        # User asked for the contact section to show icon buttons (same
        # icons as the masthead) instead of spelling out "GitHub",
        # "LinkedIn", etc. — and to be centered.
        contact_idx = self.body.find('id="contact"')
        self.assertNotEqual(contact_idx, -1, "contact section missing")
        tail = self.body[contact_idx:]

        # Should no longer spell out site names as link text
        for txt in (">GitHub<", ">LinkedIn<", ">Twitter<", ">Google Scholar<"):
            with self.subTest(removed=txt):
                self.assertNotIn(
                    txt, tail,
                    f"contact section still spells out {txt!r} — the user "
                    f"asked for icon links instead",
                )

        # Should render the same Font Awesome icons as the masthead
        for icon in (
            "fab fa-github",
            "fab fa-linkedin",
            "fab fa-twitter",
            "fas fa-graduation-cap",
            "fas fa-envelope",
        ):
            with self.subTest(icon=icon):
                self.assertIn(
                    icon, tail,
                    f"contact section missing '{icon}' icon — should "
                    f"mirror the masthead's social icon set",
                )

    def test_contact_links_are_centered(self):
        self.assertRegex(
            self.body,
            r"\.contact-links\s*\{[^}]*justify-content:\s*center",
            "about.html .contact-links should be centered via "
            "justify-content: center on the flex container",
        )
        self.assertRegex(
            self.body,
            r"\.contact-links\s*\{[^}]*display:\s*flex",
            "about.html .contact-links should use display: flex (so "
            "justify-content: center takes effect)",
        )

    def test_bio_paragraph_has_key_affiliations(self):
        # After the rewrite, the short bio should still name these.
        for needle in ("UC Berkeley", "Stanford", "Michigan", "Google X"):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.body,
                              f"bio paragraph should mention '{needle}'")


class BlogArchiveTests(unittest.TestCase):
    """The year-archive page should not render the sidebar (user asked
    for the bio + picture + links to be removed), and each post should
    render as a well-organized card with a thumbnail image."""

    def setUp(self):
        self.path = PAGES_DIR / "year-archive.html"
        self.meta, self.body = parse_front_matter(self.path)

    def test_sidebar_disabled(self):
        self.assertFalse(
            self.meta.get("author_profile"),
            "year-archive.html should have author_profile: false — the "
            "user asked for the bio/picture/links sidebar to be gone",
        )

    def test_full_width_overrides_present(self):
        # Mirror the homepage pattern so the blog cards use the full
        # content width (no 2/12 right gutter from the theme's Susy grid).
        self.assertRegex(
            self.body,
            r"\.page,\s*\.page__inner-wrap,\s*\.page__content\b",
            "year-archive.html should override .page + .page__inner-wrap "
            "+ .page__content to full width (same pattern as about.html)",
        )
        self.assertRegex(
            self.body,
            r"#main\s*\{[^}]*max-width:\s*1100px",
            "year-archive.html #main should be capped at 1100px (matches homepage)",
        )

    def test_card_renders_thumbnail(self):
        # Every post should render with a thumbnail image (user explicitly
        # asked: "Each card should have a picture as well"). The Liquid
        # fallback chain picks post.thumbnail, then header.teaser, then
        # header.image, then a site-wide default.
        self.assertIn(
            "blog-card__thumb", self.body,
            "year-archive.html cards must include a .blog-card__thumb image wrapper",
        )
        self.assertRegex(
            self.body,
            r"post\.header\.teaser",
            "year-archive.html should resolve post.header.teaser into the "
            "card thumbnail (Minimal Mistakes convention our posts use)",
        )
        self.assertRegex(
            self.body,
            r'<img\s+src="\{\{\s*thumb_url\s*\}\}"',
            "year-archive.html should render the resolved thumbnail URL "
            "in the card's <img> tag",
        )

    def test_card_has_title_date_excerpt(self):
        # A "well-organized card" has title, date, and excerpt.
        for hook, purpose in (
            ("blog-card__title", "card title"),
            ("blog-card__date", "published-on date"),
            ("blog-card__excerpt", "card excerpt"),
        ):
            with self.subTest(element=hook):
                self.assertIn(
                    hook, self.body,
                    f"year-archive.html card missing {purpose} ({hook})",
                )

    def test_card_is_clickable(self):
        # The title anchor uses a "stretched link" so the whole card is
        # a click target.
        self.assertRegex(
            self.body,
            r"\.blog-card__title\s+a::after\s*\{[^}]*position:\s*absolute",
            "year-archive.html cards should use a stretched link via "
            ".blog-card__title a::after so the whole card is clickable",
        )

    def test_no_theme_archive_single_include(self):
        # The old layout used the theme's archive-single include, which
        # doesn't render a card with an image and pulled in unwanted
        # layout (read-time, citation blocks). We now render cards inline.
        self.assertNotIn(
            "include archive-single.html", self.body,
            "year-archive.html should render custom blog cards inline, "
            "not re-use the theme's archive-single.html include",
        )


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config()
        self.author = self.cfg.get("author", {}) or {}

    def test_author_bio_is_short_role_label(self):
        self.assertEqual(
            self.author.get("bio"), "Postdoctoral Researcher",
            "author.bio should be the short role label 'Postdoctoral Researcher'",
        )

    def test_required_author_fields_populated(self):
        for key in ("name", "avatar", "email", "github", "linkedin",
                    "twitter", "googlescholar"):
            with self.subTest(field=key):
                val = self.author.get(key)
                self.assertTrue(val and str(val).strip(),
                                f"author.{key} should be set in _config.yml")

    def test_googlescholar_url_is_kareems(self):
        self.assertIn("TKfCCqQAAAAJ", self.author.get("googlescholar", ""),
                      "author.googlescholar should be Kareem's scholar URL")

    def test_publications_collection_configured(self):
        collections = self.cfg.get("collections", {}) or {}
        self.assertIn("publications", collections,
                      "publications collection must be registered in _config.yml")
        self.assertTrue(collections["publications"].get("output"),
                        "publications.output must be true so pages render")


class SiteAuthorReferenceResolutionTests(unittest.TestCase):
    """Every {{ site.author.X }} used in the templates we edited must
    resolve to a non-empty value in _config.yml."""

    def setUp(self):
        self.cfg = load_config()
        self.author = self.cfg.get("author", {}) or {}

    def _collect_refs(self, path: Path):
        text = path.read_text(encoding="utf-8")
        return set(re.findall(r"site\.author\.(\w+)", text))

    def test_masthead_refs_resolve(self):
        for field in self._collect_refs(INCLUDES_DIR / "masthead.html"):
            with self.subTest(field=field):
                self.assertTrue(
                    self.author.get(field),
                    f"masthead.html uses site.author.{field} but it's empty in _config.yml",
                )

    def test_about_refs_resolve(self):
        for field in self._collect_refs(PAGES_DIR / "about.html"):
            with self.subTest(field=field):
                self.assertTrue(
                    self.author.get(field),
                    f"about.html uses site.author.{field} but it's empty in _config.yml",
                )


class InternalLinkTests(unittest.TestCase):
    def test_resume_pdf_exists(self):
        self.assertTrue((FILES_DIR / "Resume.pdf").is_file(),
                        "files/Resume.pdf is missing — CV link will 404")

    def test_pub_thumbnails_if_referenced(self):
        # Pubs have a thumbnail: field; if the homepage ever renders it,
        # broken paths look bad. Check the referenced files exist.
        missing = []
        for p in sorted(PUBS_DIR.glob("*.md")):
            meta, _ = parse_front_matter(p)
            thumb = meta.get("thumbnail")
            if thumb:
                rel = thumb.lstrip("/")
                target = REPO / rel
                if not target.exists():
                    missing.append(f"{p.name} -> {thumb}")
        # This is informational: we simplified the homepage card to NOT
        # render thumbnails. But since the field is still there, flag them
        # so we notice if we reintroduce thumbnail rendering later.
        if missing:
            print(
                "[info] Publication thumbnail files not yet present "
                "(homepage does not render them, safe for now):",
                *("  - " + m for m in missing),
                sep="\n",
            )


class SidebarTests(unittest.TestCase):
    def setUp(self):
        self.text = (INCLUDES_DIR / "author-profile.html").read_text(encoding="utf-8")

    def test_nonfunctional_follow_button_removed(self):
        # The theme shipped a <button class="btn btn--inverse">Follow</button>
        # with no href or onclick. We removed it because it looked broken.
        self.assertNotRegex(
            self.text,
            r'<button[^>]*>\s*Follow\s*</button>',
            "sidebar still has the non-functional 'Follow' button — remove it",
        )


class PublicationActionFieldsTests(unittest.TestCase):
    """Each featured publication's front matter should declare the four
    action-URL fields (arxivurl / paperurl / codeurl / blogurl) so the
    homepage Liquid template always has something to look at (even if the
    values are empty strings). This is a regression guard: forgetting to
    add arxivurl in a new pub file would silently hide the arXiv button."""

    ACTION_FIELDS = ("arxivurl", "paperurl", "codeurl", "blogurl")

    def test_featured_pubs_declare_journal(self):
        # The redesigned pub card uses pub.journal as the clean label on
        # the first (journal) button. If unset, the Liquid falls back to
        # strip_html(pub.venue), which still works but may include "(2023,
        # 6, 325)" noise. Guard against new pubs forgetting this field.
        for p in sorted(PUBS_DIR.glob("*.md")):
            meta, _ = parse_front_matter(p)
            if not meta.get("featured"):
                continue
            with self.subTest(file=p.name):
                self.assertIn(
                    "journal", meta,
                    f"{p.name}: featured pubs should declare 'journal' "
                    f"with the clean button label (e.g. 'Communications "
                    f"Physics' or 'ICLR 2026')",
                )
                self.assertTrue(
                    str(meta["journal"]).strip(),
                    f"{p.name}: 'journal' should not be blank",
                )

    def test_featured_pubs_declare_action_fields(self):
        for p in sorted(PUBS_DIR.glob("*.md")):
            meta, _ = parse_front_matter(p)
            if not meta.get("featured"):
                continue
            for field in self.ACTION_FIELDS:
                with self.subTest(file=p.name, field=field):
                    self.assertIn(
                        field, meta,
                        f"{p.name}: featured pubs should declare '{field}' "
                        f"in front matter (use empty string if no URL yet)",
                    )


class PublicationVenueSanityTests(unittest.TestCase):
    """Spot-check venue strings so they read well after we stopped
    auto-appending the year."""

    def test_no_venue_has_trailing_comma(self):
        for p in sorted(PUBS_DIR.glob("*.md")):
            meta, _ = parse_front_matter(p)
            venue = (meta.get("venue") or "").strip()
            self.assertFalse(
                venue.endswith(","),
                f"{p.name}: venue ends with a trailing comma: {venue!r}",
            )

    def test_conference_venues_include_year(self):
        # For accepted-at-conference papers the venue should read "ICLR 2026"
        # (or similar) — year in venue, not auto-appended by Liquid.
        expected_year_in_venue = {
            "2026-04-21-zero-shot-super-resolution.md",  # ICLR 2026
            "2026-05-01-powerformer.md",                 # AISTATS 2026
        }
        for name in expected_year_in_venue:
            p = PUBS_DIR / name
            meta, _ = parse_front_matter(p)
            self.assertRegex(
                meta.get("venue", ""),
                r"\b20\d{2}\b",
                f"{name}: venue should include the year (e.g. 'ICLR 2026'), got {meta.get('venue')!r}",
            )

    def test_under_review_has_no_year(self):
        # "Under review at ICML, 2026" is awkward — future-year label.
        p = PUBS_DIR / "2026-06-01-neurde.md"
        meta, _ = parse_front_matter(p)
        venue = meta.get("venue", "")
        self.assertIn("Under review", venue,
                      f"NeurDE venue should say 'Under review at ...', got {venue!r}")
        self.assertNotRegex(
            venue, r"\b20\d{2}\b",
            f"NeurDE venue should not include a year while under review, got {venue!r}",
        )

    def test_submitted_has_no_year(self):
        p = PUBS_DIR / "2025-10-01-popcornn.md"
        meta, _ = parse_front_matter(p)
        venue = meta.get("venue", "")
        self.assertIn("Submitted", venue,
                      f"Popcornn venue should say 'Submitted to ...', got {venue!r}")
        self.assertNotRegex(
            venue, r"\b20\d{2}\b",
            f"Popcornn venue should not include a year while submitted, got {venue!r}",
        )


class EmptyStatesTests(unittest.TestCase):
    """The 'Selected Blogs' section should gracefully show an
    empty-state message when no posts are marked as featured."""

    def test_no_academicpages_placeholder_posts(self):
        # The original AcademicPages template shipped placeholder posts
        # ("2012-08-14-blog-post-1.md" etc.). Those should be gone.
        names = {p.name for p in POSTS_DIR.glob("*.md")}
        placeholders = {
            "2012-08-14-blog-post-1.md",
            "2013-08-14-blog-post-2.md",
            "2014-08-14-blog-post-3.md",
            "2015-08-14-blog-post-4.md",
        }
        leftover = names & placeholders
        self.assertFalse(leftover, f"Placeholder posts still present: {leftover}")

    def test_empty_state_fallback_present(self):
        text = (PAGES_DIR / "about.html").read_text(encoding="utf-8")
        # We included an "empty-state" <p> in both the pubs and blogs loops.
        self.assertGreaterEqual(
            text.count("empty-state"), 2,
            "about.html should render an empty-state fallback for both "
            "publications and blogs loops",
        )


if __name__ == "__main__":
    # Give useful output and a nonzero exit on failure
    unittest.main(verbosity=2)
