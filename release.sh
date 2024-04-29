#!/bin/bash

set -e

mod=$(git status --porcelain)
if [ -n "$mod" ]; then
  echo "you should commit current branch."
  exit 1
fi

current=$(git rev-parse --abbrev-ref HEAD)
branch="release/v1"

if [ "$current" == "$branch" ]; then
  git push
else
  git branch "$branch" || true
  git checkout "$branch"
  git pull
  git merge "$current"
  git push
  git checkout "$current"
fi
