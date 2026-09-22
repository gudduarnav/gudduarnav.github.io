# Verification — 22 September 2026

## Result

98 browser assertions passed. No page JavaScript errors or failed local resource requests were recorded. Eight automated WCAG A/AA scans (English/Traditional Chinese × light/dark × desktop/mobile) reported no violations. Automated checks do not establish complete accessibility conformance.

## Browser checks

Tested using Google Chrome 153.0.8010.36, Playwright 1.63.0, and axe-core 4.13.0. These were browser viewport tests on this Linux workstation, not physical iPhone or Android device tests.

- Both languages and themes checked at widths **320, 360, 390, 430, 560, 600, 768, 820, 1024, 1080, 1081, 1200, 1440, and 1920 pixels**: no horizontal page overflow or elements extending outside the viewport.
- Visual inspection of desktop and phone captures, including the hero, research cards, publications, reviewing/awards, and expanded mobile menu.
- Menu opens, transfers keyboard focus, closes after navigation, closes with Escape, and returns focus to its toggle. Section destinations clear the sticky header.
- Language switching retains the current section. Each route contains 15 publications, four education entries, and two employment entries.
- Light/dark preferences persist across reloads and language changes. With no saved choice, the theme follows the device. A manual choice takes precedence over later system changes. The switch still operates when browser storage is blocked.
- Both pages remain readable, with usable section navigation and all publications, when JavaScript is disabled.
- Both languages fit at 200% text enlargement on the tested desktop viewport. Reduced-motion mode disables smooth scrolling and transitions.
- Print styles use readable dark text on light backgrounds even after the dark theme was selected.

## Source and content checks

- HTML entrypoints and sitemap regenerate reproducibly from the shared source data.
- Local asset references and fragment links resolve; IDs are unique; each page has a single main heading.
- JavaScript syntax, structured Person metadata, XML sitemap, and whitespace checks pass.
- Reciprocal `hreflang` links and self-canonical URLs are present; `/` is the English/default route.
- All 15 author lists match publisher-deposited Crossref records. Publication DOI keys are unique.
- The books section, MCA qualification, and employment before VSM Aerospace are absent from both rendered pages and structured metadata.
- The existing private-CV ignore rule is preserved. Portrait and icon originals are unchanged.

## Delivery

The generated static website is ready for the repository's existing GitHub Pages workflow. No commit, push, or production deployment was performed during this update. The publication audit and maintainable bilingual source files are included in the repository.
