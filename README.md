# Arnav Mukhopadhyay — Research Portfolio

A bilingual, responsive academic portfolio for [gudduarnav.github.io](https://gudduarnav.github.io/), built for GitHub Pages with plain HTML, CSS, and JavaScript. No runtime dependencies, external fonts, translation service, or build service are required.

- English is the default at `/`; Taiwan Traditional Chinese is at `/zh-tw/`.
- Both pages contain the complete content before JavaScript runs and have canonical and alternate-language metadata.
- The theme initially follows the device preference. Visitors can switch light/dark themes; their choice is stored locally and shared between languages.
- A persistent desktop menu becomes an expandable menu on smaller screens. Keyboard navigation, reduced motion, print layout, and JavaScript-disabled reading are supported.

## Edit and preview

Edit `data/content.json` for the bilingual site copy and `data/publications.json` for the shared publication record. Chinese display titles and venue names are translations, while published author names and persistent identifiers retain their official spelling.

Regenerate the two HTML pages and sitemap:

```bash
python3 scripts/build.py
```

Preview the repository:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/` or `http://localhost:8000/zh-tw/`. Commit generated HTML alongside its source data so GitHub Pages can serve the site without running a build.

## Content policy

- Include verified, distinct peer-reviewed publications. Deduplicate DOI records and earlier preprints of published articles.
- Only verified peer-reviewed authored books qualify for a books section. None were identified in the September 2026 audit, so there is no books or teaching-material section.
- Retain the Springer CODEC 2019 proceedings contribution in Publications as a proceedings chapter, not as an authored book.
- The MCA qualification and employment before VSM Aerospace are intentionally excluded at the owner's request. Do not reintroduce them from public profile imports.
- Ph.D. remains in progress, expected March 2027, as confirmed by the owner on 22 September 2026.
- Verify author order and publisher metadata before updating records. Citation counts remain on linked live profiles; peer-review counts are explicitly dated.
- Cite official university announcements for university awards, with the institution's actual award wording.
- Exclude phone numbers, street addresses, and private CV files. The existing `CV_Arnav.pdf` ignore rule must remain in place.

See [the publication audit](docs/publication-audit-2026-09-22.md) and [verification notes](docs/verification.md).

## License

The website source is available under the [MIT License](LICENSE).
