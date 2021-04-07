#!/usr/bin/env bash

if [[ "$(git diff origin/master)" == "" ]]; then
    echo "No local changes detected"
    exit 1;
fi

rm results.csv

echo "Local changes: "
git diff origin/master --stat
if [[ "$(git diff)" != "" ]]; then
    git add .
fi
if [[ "$(git diff --staged)" != "" ]]; then
    echo "Please enter a summary of changes: "
    read MESSAGE
    git commit -m "$MESSAGE"
fi

git push

echo "Awaiting grade..."
while [ "$(git pull)" == "Already up to date." ]; do
    sleep 5
done

echo " "

python3 show_results.py

