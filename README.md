# SEERWORLDS_WEB

Static GitHub Pages website for **Seer Worlds** by B. Carter.

## Publish on GitHub Pages

1. Copy the contents of this folder into the root of `i4seer/SEERWORLDS_WEB`.
2. Commit and push to your normal branch (`main` is typical).
3. Open **GitHub → Settings → Pages**.
4. Choose **Deploy from a branch**.
5. Select `main` and `/ (root)`.
6. Save.

The site uses relative paths, so it works as a GitHub project page or behind a custom domain.

## Custom domain

If you use `www.seerworlds.com`, configure it in GitHub Pages after DNS is ready. GitHub can manage the `CNAME` file. This ZIP intentionally does not include a CNAME so it cannot override an existing domain setup.

## No build system required

There is no npm, framework, CDN, webfont, database, or server-side code. GitHub Pages can serve the files directly.

## Main files

- `index.html` — complete site
- `assets/styles.css` — responsive design
- `assets/script.js` — book popups, mobile nav, random-world field test
- `assets/seer-worlds-logo.webp` — optimized logo
- `assets/favicon.svg` — browser icon
- `404.html` — custom not-found page
- `.nojekyll` — plain static GitHub Pages
- `site.webmanifest`, `robots.txt`, `sitemap.xml` — web metadata
