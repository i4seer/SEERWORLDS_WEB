# Seer Worlds website

Complete deployable site.

## 2026-10-26 engraved artwork and theme

- Synced all 54 approved cover designs and their source illustrations from `C:\SEERWORLDS`. Books 1–9 use current production front covers; Books 10–54 use the approved native previews named in the source activation manifest, since older production files have not all been rebuilt. Source books are never modified or rebuilt by the website sync.
- The site follows the engraved covers: ivory paper, deep ink blue, sky blue and ochre, with the same Alegreya SC Black title font and Charter reading fonts. Web fonts and licenses are local in `assets/fonts/`.
- The homepage uses the actual Distance illustration. Individual book banners use their own source artwork; About and Journey show the Dot in illustrated scenes from Doors and Lies.
- The homepage and Books page display the six published books, followed by one development notice. Purchase URLs are preserved. News shows Memory (Book 7) in review and Shadows (Book 8) in writing. The three existing unpublished detail pages are retained for future publication but excluded from public shelves and the sitemap.
- `data/worlds-artwork.json` records source files, fingerprints, cover provenance and colors. `data/worlds-publication.json` controls the published shelf and the next two News entries.
- Refresh artwork with `python scripts/sync_worlds_artwork.py --source C:/SEERWORLDS`. Requires Pillow, fonttools and BeautifulSoup. BeautifulSoup can be installed locally with `python -m pip install --target .runtime beautifulsoup4`; `.runtime/` is ignored by Git. Use `--pages-only` after local CSS or publication changes.
- The update is local; deployment remains separate.

## 2026-10-22 author and book detail copy
- The About page uses B. Carter's personal author note with a larger opening paragraph, comfortable spacing, and a distinct signature.
- All nine book detail pages include the finished premise, hook, setting, blurb, and closing line from each book's `C:\SEERWORLDS\bookNN\images-print\background-text.txt`.
- Existing introductions, purchase links, reader questions, and navigation remain. Distance's world label now matches the current jacket copy: Bell.

## 2026-10-22 Amazon purchase links
- Followed the [Amazon series listing](https://www.amazon.com/dp/B0HF832PLR) and its product links to verify the six published books.
- Book pages offer Kindle links for books 1–6 and paperback links for books 1–3, the editions currently listed by Amazon.
- The catalog links to the Amazon series. Books 7–9 remain upcoming with no purchase links.

## 2026-10-22 hero and Dot refresh
- New river-valley hero inspired by the scenic book covers, with one glossy black Dot integrated into the artwork.
- Removed the old panorama effects, separate hero Dot overlay, and boxed callout. The mobile layout gives the image its own space above the headline.
- Homepage, About, and Journey illustrations and site icons now share the hero's glossy black Dot finish.
- Artwork: `assets/seer-worlds-river-hero.webp`, `assets/img/dot-shadow.png`, and `assets/img/dot.png`.
- Built-in image-generation prompts: [hero art direction](docs/hero-art-direction.txt) and [Dot art direction](docs/dot-art-direction.txt).

## 2026-10-22 book cover refresh
- Synced all nine featured book covers from `C:\SEERWORLDS`.
- Books 1–9 use the new scenic `images-print/cover-front.png` artwork, including the newly supplied Memory, Shadows, and Promises covers.
- Website covers remain 1280 × 2048 WebP images. Existing PNG copies and legacy placeholder assets match the current covers.
- Cover URLs include a content hash so browsers fetch updated artwork, including the existing book social previews.

## 2026-09-07 homepage update
- New full-width cinematic homepage hero.
- Hero artwork runs edge-to-edge beneath the main navigation.
- Headline, buttons, and supporting copy remain editable HTML.
- Uses the Seer Worlds reflective Dot as a separate foreground element.
- Hero language uses "Several worlds to explore" rather than a fixed world count.
- Series pillars now follow the hero before the Books section.
- Responsive desktop, tablet, and mobile hero styling included.
