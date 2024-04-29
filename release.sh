#!/bin/bash

set -e

mod=$(git status --porcelain)
if [ -n "$mod" ]; then
  echo "you should commit current branch."
  exit 1
fi

current=$(git rev-parse --abbrev-ref HEAD)
remote=origin
branch="release/v1"

if [ "$current" == "$branch" ]; then
  git push
else
  if git ls-remote --exit-code --heads "$remote" "$branch" > /dev/null 2>&1; then
    # remote 브랜치가 있음
    git fetch "$remote" "$branch"
    git checkout "$branch"
    git merge "$current"
    git push "$remote" "$branch"
  else
    # remote 브랜치가 없음
    git checkout -b "$branch"
    git push --set-upstream "$remote" "$branch"
  fi
  git checkout "$current"
fi
