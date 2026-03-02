#!/usr/bin/env python3
"""
Simple static site generator for academic/literary personal website
Supports: Markdown, LaTeX math, syntax highlighting, tags, RSS
"""

import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path
import markdown
from markdown.extensions import fenced_code, codehilite, toc, tables, meta
import shutil

class SiteGenerator:
    def __init__(self, base_dir='.'):
        self.base_dir = Path(base_dir)
        self.posts_dir = self.base_dir / 'posts'
        self.templates_dir = self.base_dir / 'templates'
        self.output_dir = self.base_dir / 'public'
        self.static_dir = self.base_dir / 'static'
        
        # Markdown processor with extensions
        self.md = markdown.Markdown(extensions=[
            'meta',
            'fenced_code',
            'codehilite',
            'toc',
            'tables',
            'footnotes'
        ])
        
    def clean_output(self):
        """Remove old build"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        
    def copy_static(self):
        """Copy static assets"""
        if self.static_dir.exists():
            shutil.copytree(self.static_dir, self.output_dir / 'static', dirs_exist_ok=True)
    
    def load_template(self, name):
        """Load HTML template"""
        template_path = self.templates_dir / f'{name}.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_config(self):
        """Load site configuration"""
        config_path = self.base_dir / 'config.yaml'
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def parse_post(self, filepath):
        """Parse markdown post with YAML frontmatter"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reset markdown processor
        self.md.reset()
        
        # Convert markdown to HTML
        html = self.md.convert(content)
        
        # Extract metadata
        metadata = {}
        if hasattr(self.md, 'Meta'):
            for key, value in self.md.Meta.items():
                metadata[key] = value[0] if len(value) == 1 else value
        
        # Generate slug from filename if not specified
        if 'slug' not in metadata:
            metadata['slug'] = filepath.stem
        
        # Parse date
        if 'date' in metadata:
            if isinstance(metadata['date'], str):
                metadata['date'] = datetime.strptime(metadata['date'], '%Y-%m-%d')
        
        # Parse tags
        if 'tags' in metadata:
            if isinstance(metadata['tags'], str):
                metadata['tags'] = [t.strip() for t in metadata['tags'].split(',')]
        else:
            metadata['tags'] = []
        
        return {
            'content': html,
            'metadata': metadata,
            'filepath': filepath
        }
    
    def get_all_posts(self):
        """Get all posts sorted by date"""
        posts = []
        for filepath in self.posts_dir.glob('*.md'):
            post = self.parse_post(filepath)
            posts.append(post)
        
        # Sort by date (newest first)
        posts.sort(key=lambda p: p['metadata'].get('date', datetime.min), reverse=True)
        return posts
    
    def render_post(self, post, template):
        """Render a single post"""
        html = template
        
        # Replace template variables
        replacements = {
            '{{title}}': post['metadata'].get('title', 'Untitled'),
            '{{date}}': post['metadata'].get('date', datetime.now()).strftime('%B %d, %Y'),
            '{{content}}': post['content'],
            '{{tags}}': ', '.join(post['metadata'].get('tags', [])),
        }
        
        for key, value in replacements.items():
            html = html.replace(key, str(value))
        
        return html
    
    def build_post_page(self, post):
        """Build individual post page"""
        template = self.load_template('post')
        html = self.render_post(post, template)
        
        # Create output directory
        post_dir = self.output_dir / 'posts' / post['metadata']['slug']
        post_dir.mkdir(parents=True, exist_ok=True)
        
        # Write HTML
        output_path = post_dir / 'index.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def build_index(self, posts):
        """Build homepage"""
        template = self.load_template('index')
        config = self.load_config()
        
        # Generate post list HTML
        post_list_html = ''
        for post in posts[:10]:  # Show latest 10
            meta = post['metadata']
            tags_html = ' '.join(f'#{tag}' for tag in meta.get('tags', []))
            post_list_html += f'''
            <article class="post-list-item">
                <h2><a href="/posts/{meta['slug']}/">{meta.get('title', 'Untitled')}</a></h2>
                <div class="post-date">{meta.get('date', datetime.now()).strftime('%Y-%m-%d')}</div>
                <p class="post-description">{meta.get('description', '')}</p>
                <div class="post-tags">{tags_html}</div>
            </article>
            '''
        
        # Replace template variables
        html = template.replace('{{posts}}', post_list_html)
        html = html.replace('{{site_title}}', config.get('title', 'Personal Site'))
        html = html.replace('{{site_description}}', config.get('description', ''))
        
        # Write homepage
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html)
    
    def build_tag_pages(self, posts):
        """Build tag index pages"""
        tags_dir = self.output_dir / 'tags'
        tags_dir.mkdir(exist_ok=True)
        
        # Collect posts by tag
        tags_dict = {}
        for post in posts:
            for tag in post['metadata'].get('tags', []):
                if tag not in tags_dict:
                    tags_dict[tag] = []
                tags_dict[tag].append(post)
        
        # Build page for each tag
        template = self.load_template('tag')
        for tag, tag_posts in tags_dict.items():
            post_list_html = ''
            for post in tag_posts:
                meta = post['metadata']
                post_list_html += f'''
                <article class="post-list-item">
                    <h2><a href="/posts/{meta['slug']}/">{meta.get('title', 'Untitled')}</a></h2>
                    <div class="post-date">{meta.get('date', datetime.now()).strftime('%Y-%m-%d')}</div>
                    <p class="post-description">{meta.get('description', '')}</p>
                </article>
                '''
            
            html = template.replace('{{tag}}', tag)
            html = html.replace('{{posts}}', post_list_html)
            
            tag_dir = tags_dir / tag.lower().replace(' ', '-')
            tag_dir.mkdir(exist_ok=True)
            with open(tag_dir / 'index.html', 'w', encoding='utf-8') as f:
                f.write(html)
    def build_sitemap(self, posts):
        """Generate sitemap.xml"""
        config = self.load_config()
        base_url = config.get('url', 'https://yoursite.vercel.app')
        base_url = base_url.rstrip('/')
        
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Homepage
        sitemap += '  <url>\n'
        sitemap += f'    <loc>{base_url}/</loc>\n'
        sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap += '    <changefreq>weekly</changefreq>\n'
        sitemap += '    <priority>1.0</priority>\n'
        sitemap += '  </url>\n'
        
        # Posts
        for post in posts:
            meta = post['metadata']
            slug = meta.get('slug')
            date = meta.get('date', datetime.now())
            
            sitemap += '  <url>\n'
            sitemap += f'    <loc>{base_url}/posts/{slug}/</loc>\n'
            sitemap += f'    <lastmod>{date.strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap += '    <changefreq>monthly</changefreq>\n'
            sitemap += '    <priority>0.8</priority>\n'
            sitemap += '  </url>\n'
        
        # Tag pages
        tags = set()
        for post in posts:
            tags.update(post['metadata'].get('tags', []))
        
        for tag in tags:
            tag_slug = tag.lower().replace(' ', '-')
            sitemap += '  <url>\n'
            sitemap += f'    <loc>{base_url}/tags/{tag_slug}/</loc>\n'
            sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap += '    <changefreq>weekly</changefreq>\n'
            sitemap += '    <priority>0.6</priority>\n'
            sitemap += '  </url>\n'
        
        sitemap += '</urlset>'
        
        with open(self.output_dir / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap)

    def build_robots_txt(self):
        """Generate robots.txt"""
        config = self.load_config()
        base_url = config.get('url', 'https://yoursite.vercel.app')
        base_url = base_url.rstrip('/')
        
        robots = f'''User-agent: *
    Allow: /

    Sitemap: {base_url}/sitemap.xml
    '''
        
        with open(self.output_dir / 'robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots)

    def build(self):
        """Build entire site"""
        print("🔨 Building site...")
        
        self.clean_output()
        print("✓ Cleaned output directory")
        
        self.copy_static()
        print("✓ Copied static assets")
        
        posts = self.get_all_posts()
        print(f"✓ Found {len(posts)} posts")
        
        for post in posts:
            self.build_post_page(post)
        print("✓ Built post pages")
        
        self.build_index(posts)
        print("✓ Built homepage")
        
        self.build_tag_pages(posts)
        print("✓ Built tag pages")

        self.build_sitemap(posts)           # ADD THIS
        print("✓ Generated sitemap.xml")    # ADD THIS

        self.build_robots_txt()             # ADD THIS
        print("✓ Generated robots.txt")     # ADD THIS
        
        print(f"\n✨ Site built successfully! Output: {self.output_dir}")

if __name__ == '__main__':
    generator = SiteGenerator()
    generator.build()
