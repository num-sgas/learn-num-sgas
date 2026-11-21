#!/usr/bin/env bash
# Builds the whole site into ./public
#   courses/<name>/  ->  /<name>/   (every folder in courses/ that has a myst.yml)
#   site/            ->  /          (gallery home page, if the folder exists)
set -euo pipefail
cd "$(dirname "$0")"

# Git Bash on Windows: don't turn BASE_URL=/name into a Windows path
export MSYS_NO_PATHCONV=1

rm -rf public
mkdir -p public

if [ -d site ]; then
  cp -r site/. public/
fi

for cfg in courses/*/myst.yml; do
  course_dir=$(dirname "$cfg")
  name=$(basename "$course_dir")
  echo "==> Building $name  ->  /$name/"
  ( cd "$course_dir" && BASE_URL="/$name" jupyter book build --html )
  mkdir -p "public/$name"
  cp -r "$course_dir/_build/html/." "public/$name/"
done

echo "==> Done. Preview with: python -m http.server -d public 8000"