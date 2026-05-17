# Statement Shield (marketing site)

Static site — works with [GitHub Pages](https://pages.github.com/) (free for public repos).

## Live URL

After you enable Pages, the site is usually:

`https://YOUR_USERNAME.github.io/REPO_NAME/`

Update `index.html`, `robots.txt`, and `sitemap.xml` when you have a real domain (or keep the GitHub URL in `canonical` if you prefer).

## Enable GitHub Pages

1. Push this folder to a new GitHub repository.
2. On GitHub: **Settings → Pages**.
3. **Build and deployment**: Source = **Deploy from a branch**.
4. **Branch**: `main` (or `master`), folder **`/ (root)`**, Save.
5. Wait a minute; refresh Pages — copy the published URL.

## Edit the site

| Where | How |
|--------|-----|
| This PC | Change files in this folder, commit, `git push`. |
| GitHub | Open a file in the repo → **Edit** (pencil) → commit. |
| Cursor / VS Code | Same as local: edit, Source Control, push. |

The server only serves what is in the repo; there is no WordPress-style admin panel.

## Local preview

Use `Serve-Local.bat` or `Serve-Local.ps1` (Python on `127.0.0.1:8080`).

## First-time push (replace placeholders)

```bash
cd path/to/Statement-Shield-Website
git init
git add .
git commit -m "Initial Statement Shield site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Then turn on Pages in repo settings as above.
