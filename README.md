# Personal Website Setup Instructions

## Overview
This is a minimal static site generator built in Python, inspired by Gwern's clean aesthetic. It supports:
- Markdown posts with YAML frontmatter
- LaTeX math rendering (KaTeX)
- Syntax highlighting for code
- Tag-based filtering
- Single-column, distraction-free layout
- Clean typography with generous whitespace

## Prerequisites
- Python 3.7+
- pip (Python package manager)

## Installation Steps

### 1. Install Required Python Packages

```bash
pip install markdown pyyaml
```

### 2. Directory Structure

Your site should have this structure:

```
personal-site/
├── build.py              # Site generator script
├── config.yaml           # Site configuration
├── posts/                # Your markdown posts go here
│   ├── example-stats-post.md
│   └── example-book-review.md
├── templates/            # HTML templates
│   ├── index.html
│   ├── post.html
│   └── tag.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── book-placeholder.jpg
└── public/               # Generated site (created by build.py)
```

### 3. Configuration

Edit `config.yaml` with your information:

```yaml
title: "Your Name"
description: "Statistics, research, books, and poetry"
url: "https://yourusername.github.io"

currently_reading:
  title: "Book Title"
  author: "Author Name"
  cover: "/static/images/book-cover.jpg"
  note: "Your thoughts on the book"
```

### 4. Writing Posts

Create markdown files in the `posts/` directory. Each post needs YAML frontmatter at the top:

```markdown
---
title: "Understanding the Central Limit Theorem"
date: 2026-02-27
tags: research, statistics
description: "A gentle introduction to one of statistics' most important theorems"
slug: central-limit-theorem
---

Your content here...

## LaTeX Math Examples

Inline math: $\bar{X} = \frac{1}{n}\sum_{i=1}^{n} X_i$

Display math:
$$
\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} N(0, \sigma^2)
$$

## Code Examples

```python
import numpy as np
import matplotlib.pyplot as plt

# Generate samples
samples = np.random.normal(0, 1, 1000)
plt.hist(samples)
```

Regular markdown formatting works: **bold**, *italic*, [links](https://example.com)
```

### 5. Building the Site

Run the build script:

```bash
cd personal-site
python build.py
```

This generates your site in the `public/` directory.

### 6. Preview Locally

To preview your site:

```bash
cd public
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

## Publishing Options

### Option A: GitHub Pages (Recommended)

1. Create a GitHub repository named `yourusername.github.io`
2. Add all files to the repository
3. Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Site

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install markdown pyyaml
      
      - name: Build site
        run: python build.py
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

4. In your repo settings, enable GitHub Pages and set source to "gh-pages" branch
5. Every time you push changes, the site rebuilds automatically

### Option B: Netlify

1. Sign up at netlify.com
2. Connect your GitHub repository
3. Set build command: `pip install markdown pyyaml && python build.py`
4. Set publish directory: `public`

### Option C: Manual Upload

Just upload the contents of the `public/` folder to any web host.

## Workflow Tips

### Adding New Posts

1. Create a new `.md` file in `posts/`
2. Add YAML frontmatter
3. Write your content
4. Run `python build.py`
5. Push to GitHub (if using GitHub Pages)

### Using Tags

Add tags to any post:
```yaml
tags: research, statistics, bayesian
```

or
```yaml
tags: books, poetry, literary-criticism
```

Tag pages are automatically generated at `/tags/tag-name/`

### Adding Images to Posts

1. Put images in `static/images/`
2. Reference in markdown: `![Alt text](/static/images/your-image.jpg)`

## Customization

### Changing Colors/Fonts

Edit `static/css/style.css`, particularly the `:root` variables:

```css
:root {
    --text-primary: #1a1a1a;    /* Main text color */
    --accent: #2c5282;           /* Link color */
    --font-serif: 'Georgia', serif;
}
```

### Modifying Layout

Templates are in `templates/`:
- `index.html` - Homepage
- `post.html` - Individual post pages
- `tag.html` - Tag archive pages

### Adding Pages

For static pages (like About), create `content/about.md` and you'll need to add a simple function to `build.py` to process them. I can help with this if needed.

## Troubleshooting

**"Module not found" errors**: Run `pip install markdown pyyaml`

**Math not rendering**: Check that your post content has `$...$` for inline math and `$$...$$` for display math

**Code not highlighting**: Make sure you're using triple backticks with language name:
````
```python
your code here
```
````

**Site looks broken**: Make sure you're viewing from a web server (not just opening HTML files directly)

## Next Steps

1. Customize `config.yaml` with your info
2. Write a few sample posts
3. Build and preview locally
4. Set up GitHub Pages
5. Start writing!

Let me know if you hit any issues or want to customize anything further.
