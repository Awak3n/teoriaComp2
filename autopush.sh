#!/bin/bash

echo commit message:
read var
git checkout master
git pull
git checkout dev
git add .
git commit -m "$var"
git merge dev master
git checkout master
git merge master dev
git push
git checkout dev
