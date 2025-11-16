#!/bin/bash
# Wiki Setup Script
# Publishes wiki pages to GitHub

echo "========================================="
echo "  WIKI SETUP - Reactive Light Show"
echo "========================================="
echo ""

# Check if first page exists
echo "📝 Step 1: Create the first wiki page"
echo ""
echo "Please do this manually (one-time setup):"
echo "1. Open: https://github.com/ebman/reactive-screen/wiki"
echo "2. Click 'Create the first page'"
echo "3. Title: Home"
echo "4. Copy the content from: wiki/Home.md"
echo "5. Click 'Save Page'"
echo ""
read -p "Press ENTER when you've created the Home page..."

echo ""
echo "🔄 Step 2: Cloning wiki repository..."

cd /home/ebernard
if [ -d "reactive-screen.wiki" ]; then
    rm -rf reactive-screen.wiki
fi

git clone https://github.com/ebman/reactive-screen.wiki.git

if [ ! -d "reactive-screen.wiki" ]; then
    echo "❌ Failed to clone wiki. Make sure you created the first page."
    exit 1
fi

echo "✅ Wiki cloned successfully"
echo ""
echo "📄 Step 3: Copying wiki pages..."

cd reactive-screen.wiki

# Copy all wiki markdown files
cp ../reactive-screen/wiki/Quick-Start.md .
cp ../reactive-screen/wiki/Installation-Guide.md .
cp ../reactive-screen/wiki/Visual-Effects-Reference.md .
cp ../reactive-screen/wiki/FAQ.md .

echo "✅ Wiki pages copied"
echo ""
echo "📤 Step 4: Publishing to GitHub..."

git add *.md
git commit -m "Add comprehensive wiki documentation

- Quick Start guide
- Installation Guide for all distros
- Visual Effects Reference
- FAQ with troubleshooting
"

git push origin master

echo ""
echo "========================================="
echo "  ✅ WIKI PUBLISHED!"
echo "========================================="
echo ""
echo "View your wiki at:"
echo "https://github.com/ebman/reactive-screen/wiki"
echo ""
