#!/bin/bash

# Exit on error
set -e

echo "🚀 Preparing to push to Git..."

# Initialize git repository if not done
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add files to git (respecting .gitignore)
echo "Staging files..."
git add .

# Set branch name to main
echo "Setting branch to main..."
git branch -M main

# Committing files
COMMIT_MSG="Initial commit: Weather Alert WebApp (Django + Telegram)"
echo "Committing files with message: '$COMMIT_MSG'..."

# Check if there is a HEAD commit or any changes to commit
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    # First commit
    git commit -m "$COMMIT_MSG"
else
    # Subsequent commits
    if git diff-index --quiet HEAD --; then
        echo "No changes to commit."
    else
        git commit -m "$COMMIT_MSG"
    fi
fi

# Add or update remote origin
REMOTE_URL="https://github.com/harys-rifai/wether-apps.git"
if git remote | grep -q "^origin$"; then
    echo "Updating existing remote origin URL to $REMOTE_URL..."
    git remote set-url origin "$REMOTE_URL"
else
    echo "Adding remote origin $REMOTE_URL..."
    git remote add origin "$REMOTE_URL"
fi

# Push to git
echo "Pushing to GitHub (main branch)..."
git push -u origin main

echo "✅ Push script completed!"
