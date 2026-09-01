# -*- coding: utf-8 -*-
"""重建单文件版：将目录版 index.html 的图片/音频/字体全部内嵌为 base64 data URI"""
import base64, glob, os

BASE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(BASE, 'index.html')
out = os.path.join(BASE, '一轮月万家灯_交互式漫画.html')

html = open(src, 'r', encoding='utf-8').read()

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

# images: s01_cover .. s13_moon, plus any sXX*.jpg used
img_files = sorted(glob.glob(os.path.join(BASE, 'images', 's*.jpg')))
for ip in img_files:
    name = os.path.basename(ip)
    # html references like "s01_cover.jpg" (IMG prefix concatenation)
    pat = '"' + name + '"'
    if pat in html:
        html = html.replace(pat, '"data:image/jpeg;base64,' + b64(ip) + '"')
        print('img embedded:', name)
    else:
        print('WARN not referenced:', name)

# audio
ap = os.path.join(BASE, 'audio', 'bgm.wav')
if 'src="audio/bgm.wav"' in html:
    html = html.replace('src="audio/bgm.wav"', 'src="data:audio/wav;base64,' + b64(ap) + '"')
    print('audio embedded')

# font
fp = os.path.join(BASE, 'fonts', 'lxgw-wenkai-subset.woff2')
if "url('fonts/lxgw-wenkai-subset.woff2')" in html:
    html = html.replace("url('fonts/lxgw-wenkai-subset.woff2')", "url('data:font/woff2;base64," + b64(fp) + "')")
    print('font embedded')
else:
    print('WARN font ref not found')

# IMG prefix -> inline data URIs already present
html = html.replace('var IMG = "images/";', 'var IMG = "";')

open(out, 'w', encoding='utf-8').write(html)
print('written:', out, os.path.getsize(out) / 1048576, 'MB')
