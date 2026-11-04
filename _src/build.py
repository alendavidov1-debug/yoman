import re, os, json, hashlib
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
s = open('_src/app.html').read()
head_end = s.index('<body>\n') + len('<body>\n')
wrapper_head = s[:head_end]
body = s[head_end:]
assert body.rstrip().endswith('</body></html>')
body = body.rstrip()[:-len('</body></html>')]
# --- site/index.html ---
fonts = open('_src/rubik.css').read().replace('url(fonts/', 'url(fonts/')
fonts = re.sub(r"url\(fonts/(rubik-\w+\.woff2)\)", r"url(fonts/\1)", fonts)
pb = body.replace('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
pb = pb.replace('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap">', '<style>' + fonts + '</style>')
assert 'googleapis' not in pb
pb = pb.replace('<title>One Way Up</title>\n', '').replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
files = sorted([os.path.join(dp, f)[2:] for dp, _, fs in os.walk('.') if not dp.startswith(('./.git', './_src')) for f in fs if f not in ('index.html', 'sw.js', '.nojekyll', 'version.json', 'README.md')])
ver = hashlib.sha1((pb + json.dumps(files)).encode()).hexdigest()[:10]
head = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>One Way Up</title>
<meta name="theme-color" content="#17181b">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="One Way Up">
<meta name="format-detection" content="telephone=no">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="preload" href="fonts/rubik-hebrew.woff2" as="font" type="font/woff2" crossorigin>
<style>:root{{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}html{{scroll-padding-top:env(safe-area-inset-top,0px);-webkit-text-size-adjust:100%}}body{{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000;overscroll-behavior-y:none}}img{{max-width:100%}}[hidden]:not([hidden=until-found i]){{display:none!important}}</style>
<script>window.__APPVER="{ver}";if("serviceWorker"in navigator&&isSecureContext)addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{{}}));</script>
</head><body>
'''
open('index.html', 'w').write(head + pb + '\n</body></html>\n')
manifest = {"name": "One Way Up", "short_name": "One Way Up", "lang": "he", "dir": "rtl", "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait", "background_color": "#17181b", "theme_color": "#17181b", "id": "./",
  "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
open('manifest.webmanifest', 'w').write(json.dumps(manifest, ensure_ascii=False, indent=1))
shell = ["./", "index.html", "manifest.webmanifest", "fonts/rubik-hebrew.woff2", "fonts/rubik-latin.woff2", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"]
imgs = [f for f in files if f.startswith(('ex/', 'ek/'))]
sw = open('_src/sw.js').read().replace('__VER__', ver).replace('__SHELL__', json.dumps(shell)).replace('__IMGS__', json.dumps(imgs))
open('sw.js', 'w').write(sw)
open('.nojekyll', 'w').write('')
print('ver', ver, 'imgs', len(imgs))

open('version.json', 'w').write(json.dumps({'v': ver}))
