# SEERWORLDS_WEB — Professional GitHub Pages Site

This is a complete static website matching the approved visual direction:
cinematic fantasy hero, overlay navigation, torn parchment sections, navy/gold
branding, illustrated book row, and consistent styling across every page.

## Pages
- Home
- Worlds
- Books
- The Journey
- Meet the Dot
- About
- Other Series
- News
- Contact
- 9 individual book pages
- Custom 404

## Publish
Copy the contents of this ZIP into the root of:
`i4seer/SEERWORLDS_WEB`

Then enable:
GitHub → Settings → Pages → Deploy from a branch → main → /(root)

No build process, npm, framework, or server is required.

## Contact form
The included contact form uses `mailto:` because GitHub Pages is static.
Replace the form `action` later with Formspree/Basin/your own endpoint if desired.

## Clean URLs
All public pages now use directory-based clean URLs. Root pages such as `/about`, `/worlds`, `/books`, `/journey`, `/dot`, `/news`, `/other-series`, and `/contact` are served from matching `<page>/index.html` files. Book detail pages use the same pattern under `/books/<title>/index.html`. Legacy `.html` files are retained only as redirects to the clean URLs.
