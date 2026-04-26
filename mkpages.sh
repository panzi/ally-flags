#!/usr/bin/bash

set -eo pipefail

./mkhtml.py

git checkout gh-pages

mv dist/* .

git add *.svg *.html *.css *.js *.png
git commit -m "updated gh-pages"
git push
git checkout main
