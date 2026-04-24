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
  - Internal links in about.md (e.g., /files/Resume.pdf) point to files
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
        text = (PAGES_DIR / "about.md").read_text(encoding="utf-8")
        o, c = count_liquid_tags(text)
        self.assertEqual(o, c, f"about.md has unbalanced Liquid tags: {o} opens vs {c} closes")

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
        # URL -> what we expect to exist in the repo
        checks = {
            "/": PAGES_DIR / "about.md",
            "/publications/": PAGES_DIR / "publications.md",
            "/year-archive/": PAGES_DIR / "year-archive.html",
            "/files/Resume.pdf": FILES_DIR / "Resume.pdf",
        }
        for item in self.main:
            url = item["url"]
            if url == "/#contact":
                # anchor on homepage; check the anchor exists in about.md
                about = (PAGES_DIR / "about.md").read_text(encoding="utf-8")
                self.assertIn('id="contact"', about,
                              "about.md is missing the #contact anchor")
                continue
            target = checks.get(url)
            self.assertIsNotNone(target, f"Unexpected nav URL: {url}")
            self.assertTrue(target.exists(),
                            f"Nav '{item['title']}' points to {url}, but {target} does not exist")


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

    def test_spacer_cell_present(self):
        # The spacer <li> with width: 100% is what pushes nav links to the
        # right side under the theme's display: table layout.
        self.assertIn("masthead__menu-item--spacer", self.text,
                      "masthead.html missing the spacer <li> that right-aligns nav")

    def test_spacer_cell_has_full_width(self):
        self.assertRegex(
            self.text,
            r"\.masthead__menu-item--spacer\b[^}]*width:\s*100%",
            "masthead.html spacer cell must have width: 100% to push nav right",
        )

    def test_does_not_override_to_flex(self):
        # Earlier version forced display: flex which broke greedy-nav JS
        # (it compares $vlinks.width() to the nav width). Make sure we're
        # not reintroducing that override.
        self.assertNotRegex(
            self.text,
            r"\.visible-links\s*\{[^}]*display:\s*flex",
            "masthead.html overrides .visible-links to display: flex — that "
            "breaks the greedy-nav overflow JS. Use display: table + spacer instead.",
        )

    def test_iterates_navigation_data(self):
        self.assertIn("site.data.navigation.main", self.text,
                      "masthead.html should iterate site.data.navigation.main")


class AboutPageTests(unittest.TestCase):
    def setUp(self):
        self.text = (PAGES_DIR / "about.md").read_text(encoding="utf-8")
        self.meta, self.body = parse_front_matter(PAGES_DIR / "about.md")

    def test_permalink_is_root(self):
        self.assertEqual(self.meta.get("permalink"), "/",
                         "about.md permalink should be '/'")

    def test_author_profile_enabled(self):
        self.assertTrue(self.meta.get("author_profile"),
                        "about.md should have author_profile: true so sidebar renders")

    def test_required_sections(self):
        for heading in ("Selected Publications", "Selected Blogs",
                        "Curriculum Vitae", "Get in touch"):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.body,
                              f"about.md missing required section: {heading}")

    def test_no_dissertation_content(self):
        # User asked to remove dissertation-related content from the bio.
        self.assertNotRegex(self.body, r"(?i)\bdissertation\b",
                            "about.md still references 'dissertation' — the user asked to remove this")

    def test_featured_pub_liquid_loop(self):
        # Exact filter chain we committed: where featured true, sort date, reverse
        self.assertRegex(
            self.body,
            r'site\.publications\s*\|\s*where:\s*"featured",\s*true\s*\|\s*sort:\s*"date"\s*\|\s*reverse',
            "about.md is missing the featured-publications filter chain",
        )

    def test_featured_posts_liquid_loop(self):
        self.assertRegex(
            self.body,
            r'site\.posts\s*\|\s*where:\s*"featured",\s*true',
            "about.md is missing the featured-posts filter chain",
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

    def test_no_auto_year_append_in_venue_line(self):
        # Earlier version appended ", {{ pub.date | date: '%Y' }}" to the
        # venue — awkward for "Under review at ICML, 2026". We now encode
        # year into the venue string itself.
        self.assertNotRegex(
            self.body,
            r'\{\{\s*pub\.venue\s*\}\}[^<]*\{\%\s*if\s+pub\.date',
            "about.md should not auto-append the year to the venue line",
        )

    def test_cv_download_link(self):
        self.assertIn("/files/Resume.pdf", self.body,
                      "about.md is missing the CV download link")

    def test_contact_email_uses_site_author(self):
        self.assertIn("{{ site.author.email }}", self.body,
                      "about.md contact should use {{ site.author.email }}")

    def test_bio_paragraph_has_key_affiliations(self):
        # After the rewrite, the short bio should still name these.
        for needle in ("UC Berkeley", "Stanford", "Michigan", "Google X"):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.body,
                              f"bio paragraph should mention '{needle}'")


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
        for field in self._collect_refs(PAGES_DIR / "about.md"):
            with self.subTest(field=field):
                self.assertTrue(
                    self.author.get(field),
                    f"about.md uses site.author.{field} but it's empty in _config.yml",
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
    """Sanity: since there are no blog posts yet, the 'Selected Blogs'
    section should gracefully show the empty-state message."""

    def test_posts_dir_is_empty(self):
        posts = list(POSTS_DIR.glob("*.md"))
        self.assertEqual(posts, [],
                         f"_posts should be empty (placeholders removed), found {posts}")

    def test_empty_state_fallback_present(self):
        text = (PAGES_DIR / "about.md").read_text(encoding="utf-8")
        # We included an "empty-state" <p> in both the pubs and blogs loops.
        self.assertGreaterEqual(
            text.count("empty-state"), 2,
            "about.md should render an empty-state fallback for both "
            "publications and blogs loops",
        )


if __name__ == "__main__":
    # Give useful output and a nonzero exit on failure
    unittest.main(verbosity=2)
