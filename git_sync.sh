#!/usr/bin/env bash

set -x

git stash
git pull
git push
git stash pop
