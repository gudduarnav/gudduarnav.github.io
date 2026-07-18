# Arnav Mukhopadhyay — Research Portfolio

Source for [gudduarnav.github.io](https://gudduarnav.github.io/), a privacy-conscious academic portfolio covering 6G near-field wireless research, publications, education, experience, scholarly service, books, and verified profile links.

## Content policy

- The current local CV is the primary source for non-public academic history, education, skills, and employment.
- DOI, ORCID, DBLP, IEEE, conference, publisher, and public professional records are used to verify and supplement current information.
- Duplicate preprints are not counted as separate publications after a peer-reviewed version is available.
- Volatile citation counts are intentionally not hard-coded; visitors are directed to live scholarly profiles.
- Phone numbers, postal codes, street addresses, and other private address details are excluded.
- `CV_Arnav.pdf` is ignored because the local source copy contains private contact details and must not be deployed.

## Local preview

Run a static server from the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Maintenance

When updating the portfolio:

1. Reconcile new CV entries with current DOI and ORCID metadata.
2. Deduplicate preprints and final publications.
3. Verify author order, venue, volume, pages, year, and DOI.
4. Update the visible revision date and `sitemap.xml`.
5. Confirm that no phone number or private address appears in tracked files.

## License

The website source is available under the [MIT License](LICENSE).
