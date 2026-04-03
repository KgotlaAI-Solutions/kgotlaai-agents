#!/bin/bash
# Kgotla AI SSL Fix Script
# Run this after updating your repository

echo "🔧 Kgotla AI SSL Fix Script"
echo "============================"

# Check if in git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run from your website root."
    exit 1
fi

echo ""
echo "Step 1: Finding HTTP references..."
echo "-----------------------------------"

# Find and list all HTTP references
echo "Files with http:// references:"
grep -r "http://" . --include="*.html" --include="*.css" --include="*.js" -l 2>/dev/null | head -20

echo ""
echo "Step 2: Replacing HTTP with HTTPS..."
echo "-------------------------------------"

# Replace http:// with https:// in HTML files
find . -name "*.html" -type f -exec sed -i 's/http:\/\//https:\/\//g' {} +
echo "✅ Updated HTML files"

# Replace in CSS files
find . -name "*.css" -type f -exec sed -i 's/http:\/\//https:\/\//g' {} +
echo "✅ Updated CSS files"

# Replace in JS files
find . -name "*.js" -type f -exec sed -i 's/http:\/\//https:\/\//g' {} +
echo "✅ Updated JS files"

echo ""
echo "Step 3: Checking for remaining HTTP references..."
echo "--------------------------------------------------"

remaining=$(grep -r "http://" . --include="*.html" --include="*.css" --include="*.js" -l 2>/dev/null | wc -l)

if [ "$remaining" -eq 0 ]; then
    echo "✅ No HTTP references found!"
else
    echo "⚠️  Found $remaining files with HTTP references:"
    grep -r "http://" . --include="*.html" --include="*.css" --include="*.js" -l 2>/dev/null
fi

echo ""
echo "Step 4: Git status..."
echo "---------------------"
git status --short

echo ""
echo "Next steps:"
echo "1. Review the changes: git diff"
echo "2. Stage changes: git add ."
echo "3. Commit: git commit -m 'Fix: Update all HTTP to HTTPS'"
echo "4. Push: git push origin main"
echo "5. Wait for deployment (2-5 minutes)"
echo "6. Test: https://kgotlaai.co.za"
echo ""
echo "Done! ✅"
