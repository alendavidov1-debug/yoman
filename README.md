# יומן מתאמן PWA

Live: https://alendavidov1-debug.github.io/yoman/ (GitHub Pages, branch `main`, root).

**This repo is the app's source of truth.** The old claude.ai artifact is no longer updated.

## Make a change
1. Edit `_src/app.html` (the whole app: HTML, CSS, JS in one file).
2. Run `python3 _src/build.py` from the repo root. It writes `index.html`, `sw.js`, `manifest.webmanifest`, `version.json`.
3. Commit and push to `main`. Pages deploys in ~1 minute.

## How the phone gets the update
- `sw.js` changes on every build, so the service worker reinstalls.
- `index.html` is network-first (3 s timeout, then cache), so it works offline.
- The app checks `version.json` on start and when it returns to the foreground. If the version changed and no workout is open, it reloads itself. During a workout it waits.
- Manual: מטרות ← המטרה שלי ← גיבוי ונתונים ← "בדיקת עדכון".

## Data
User data never goes in this repo. It lives on the device (IndexedDB `yoman`) and in the user's own JSON backups.
