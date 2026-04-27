#!/usr/bin/env python3

import os
import json

from os.path import join as join_path, splitext
from xml.etree import ElementTree as ET
from html import escape
from shutil import copy
from subprocess import check_call

from PIL import Image

FLAGS = [
    "ally-flag.svg",
    "ally-flag-starfleet.svg",
    "ally-flag-klingon.svg",
    "ally-flag-stargate.svg",
    "ally-flag-triforce.svg",
    "ally-flag-arch.svg",
]

def _inner_xml(element: ET.Element, buf: list[str]) -> None:
    text = element.text
    tag = element.tag

    # WTF!?
    if tag.startswith('{'):
        tag = tag[tag.find('}') + 1:]

    buf.append('<')
    buf.append(tag)
    for key, value in element.attrib.items():
        if key != "id":
            buf.append(' ')
            buf.append(escape(key))
            buf.append('="')
            buf.append(escape(value))
            buf.append('"')
    buf.append('>')

    if text:
        buf.append(escape(text))

    for child in element:
        _inner_xml(child, buf)
        tail = child.tail
        if tail:
            buf.append(escape(tail))

    buf.append('</')
    buf.append(tag)
    buf.append('>')

def inner_xml(element: ET.Element) -> str:
    buf: list[str] = []
    _inner_xml(element, buf)
    return "".join(buf)

def main() -> None:
    os.makedirs("dist", exist_ok=True)
    copy("style.css", join_path("dist", "style.css"))
    copy("script.js", join_path("dist", "script.js"))

    with open(join_path("dist", "index.html"), "w") as indexfp:
        indexfp.write(
f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ally Flag Variations</title>

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Some variations on the LGBTQIA+ ally flag/straight ally pride flag, just for fun.">
<meta name="author" content="Mathias Panzenböck">
<meta property="og:image" content="https://panzi.github.io/ally-flags/preview.png">
<meta property="og:image:width" content="288">
<meta property="og:image:height" content="192">

<link rel="stylesheet" href="style.css">
</head>
<body data-flags="{escape(' '.join(splitext(flag)[0] for flag in FLAGS))}">
<h1>Ally Flag Variations</h1>
<main>
<p>Some variations on the LGBTQIA+ ally flag/straight ally pride flag, just for fun.</p>
<ul class="flags">
""")
        for flag in FLAGS:
            print(flag)
            copy(flag, join_path("dist", flag))

            basename = splitext(flag)[0]
            flag_png = f"{basename}.png"

            check_call([
                "inkscape",
                "--export-area-page",
                "--export-type=png",
                "--export-png-color-mode=RGB_8",
               f"--export-filename={join_path("dist", flag_png)}",
                flag,
            ])

            doc = ET.parse(flag)

            title_el = doc.find("./{http://www.w3.org/2000/svg}title")
            assert title_el is not None

            title = title_el.text
            assert title is not None

            desc_el = doc.find("./{http://www.w3.org/2000/svg}desc")
            assert desc_el is not None

            desc = inner_xml(desc_el)

            indexfp.write(
f"""\
<li class="flag" id="flag-{escape(basename)}">
    <figure>
        <img src="{escape(flag)}" onclick="openDialog({escape(json.dumps(basename))})">
        <figcaption>
            <div class="downloads">
                <span class="downloads-label">Download:</span>
                <a class="download download-svg" download="{escape(basename)}.svg" href="{escape(flag)}">SVG</a>
                <a class="download download-png" download="{escape(basename)}.png" href="{escape(flag_png)}">PNG</a>
            </div>
            <p>{desc}</p>
        </figcaption>
    </figure>
</li>
""")

        indexfp.write(
"""\
</ul>
<dialog id="dialog">
    <img id="dialog-img">
    <button type="button" id="dialog-prev" class="dialog-nav dialog-prev" title="Previous"><span>‹</span></button>
    <button type="button" id="dialog-next" class="dialog-nav dialog-next" title="Next"><span>›</span></button>
    <button class="dialog-close" command="close" commandfor="dialog" title="Close">
        &times;
    </button>
</dialog>
<small>
<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de">CC-BY-SA 4.0</a> 2026 Mathias Panzenböck – <a href="https://github.com/panzi/ally-flags">GitHub</a>
</small>
</main>
<script type="text/javascript" async src="script.js"></script>
</body>
</html>
""")

    preview_path = join_path('dist', 'preview.png')
    print(preview_path)

    tile_width = 288
    tile_height = 192
    margin = 40

    images = [Image.open(join_path('dist', splitext(flag)[0] + '.png')).resize((tile_width, tile_height)) for flag in FLAGS]
    preview = Image.new('RGB', (tile_width * 3 + margin * 4, tile_height * 2 + margin * 3), 0x0F0F0F)

    for column in range(2):
        for row in range(3):
            image = images[column * 3 + row]
            preview.paste(image, (margin + row * (tile_width + margin), margin + column * (tile_height + margin)))

    preview.save(preview_path)

if __name__ == '__main__':
    main()
