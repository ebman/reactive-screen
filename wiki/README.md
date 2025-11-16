# Wiki Content

This folder contains wiki pages for the Reactive Multi-Monitor Light Show.

## Pages Created

- **Home.md** - Wiki home page with navigation
- **Quick-Start.md** - 5-minute getting started guide
- **Installation-Guide.md** - Complete installation for all distros
- **Visual-Effects-Reference.md** - Detailed effects documentation
- **FAQ.md** - Frequently asked questions

## How to Upload to GitHub Wiki

### Option 1: Manual Upload (Easy)

1. Go to https://github.com/ebman/reactive-screen/wiki
2. Click "Create the first page" or "New Page"
3. Copy content from each `.md` file
4. Paste into GitHub wiki editor
5. Save each page

### Option 2: Git Clone (Advanced)

Once you've created the first page through the web interface, you can use git:

```bash
# Clone the wiki repository
git clone https://github.com/ebman/reactive-screen.wiki.git

# Copy wiki files
cp wiki/*.md reactive-screen.wiki/

# Commit and push
cd reactive-screen.wiki
git add *.md
git commit -m "Add comprehensive wiki documentation"
git push origin master
```

## Creating Additional Pages

Feel free to add more pages:
- Monitor-Configuration.md
- Customization-Guide.md
- Performance-Tuning.md
- Troubleshooting.md
- Contributing.md
- Architecture.md
- Audio-Analysis.md
- Gallery.md

Use the same markdown format as the existing pages.
