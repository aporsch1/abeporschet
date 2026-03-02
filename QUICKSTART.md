# Quick Start Guide

## Getting Started (5 minutes)

1. **Install Python dependencies:**
   ```bash
   pip install markdown pyyaml
   ```

2. **Customize your site:**
   Edit `config.yaml`:
   - Change "Your Name" to your actual name
   - Update the description
   - Add your email/social links

3. **Build the site:**
   ```bash
   python build.py
   ```

4. **Preview locally:**
   ```bash
   cd public
   python -m http.server 8000
   ```
   Open http://localhost:8000

## Publishing to GitHub Pages

1. **Create a GitHub repository:**
   - Name it `yourusername.github.io` (replace yourusername with your GitHub username)
   - Make it public

2. **Push your code:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to your repository settings
   - Click "Pages" in the sidebar
   - Under "Build and deployment" → Source: choose "GitHub Actions"
   - The workflow will run automatically

4. **Wait a minute**, then visit `https://yourusername.github.io`

## Writing a New Post

Create a file in `posts/` like `my-new-post.md`:

```markdown
---
title: "My Post Title"
date: 2026-02-27
tags: research, statistics
description: "A brief description"
slug: my-new-post
---

Your content here!

## Math works

The mean is $\bar{x} = \frac{1}{n}\sum x_i$

## Code works

```python
import pandas as pd
df = pd.read_csv('data.csv')
```

Regular **markdown** formatting works too.
```

Then run `python build.py` and push to GitHub.

## Common Tasks

### Change site colors:
Edit `static/css/style.css` → `:root` variables

### Add images to a post:
1. Put image in `static/images/your-image.jpg`
2. Reference in markdown: `![Description](/static/images/your-image.jpg)`

### Filter posts by tag:
Posts automatically appear at `/tags/tag-name/`

## File Structure at a Glance

```
personal-site/
├── build.py          # Run this to build the site
├── config.yaml       # Edit your site info here
├── posts/            # Write your posts here
│   └── *.md
├── static/           # CSS, images, etc
└── public/           # Generated site (don't edit)
```

## Troubleshooting

**Site looks broken locally?**
- Make sure you're using `python -m http.server`, not just opening HTML files

**Math not rendering?**
- Check you're using `$...$` or `$$...$$`, not `\(...\)` or `\[...\]`

**GitHub Pages not updating?**
- Check the "Actions" tab in your repo to see if build succeeded
- Make sure you enabled GitHub Pages in settings with "GitHub Actions" as source

**Changes not showing?**
- Did you rebuild? Run `python build.py`
- Did you push to GitHub? Run `git push`

## Next Steps

1. Customize config.yaml with your actual info
2. Delete or modify the example posts
3. Write your first post
4. Push to GitHub
5. Share your site!

Questions? Issues? The README.md has more detailed documentation.
