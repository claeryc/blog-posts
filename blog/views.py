import os
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
import markdown
import yaml

def parse_front_matter(filepath):
    """Read YAML front matter from a Markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().split('---')
        if len(lines) >= 3:
            meta = yaml.safe_load(lines[1])
            return meta
    return {}

def index(request):
    posts_dir = os.path.join(settings.BASE_DIR, 'blog', 'posts')
    files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
    posts = []
    for filename in sorted(files, reverse=True):
        filepath = os.path.join(posts_dir, filename)
        meta = parse_front_matter(filepath)
        slug = filename[:-3]
        posts.append({
            'slug': slug,
            'title': meta.get('title', slug),
            'thumbnail': meta.get('thumbnail', '/static/images/default.jpg')
        })

    per_page = 2
    page_str = request.GET.get('page', '1')
    try:
        page = int(page_str)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    start = (page - 1) * per_page
    end = start + per_page
    paginated_posts = posts[start:end]

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if end < len(posts) else None

    return render(request, 'blog/index.html', {
        'posts': paginated_posts,
        'prev_page': prev_page,
        'next_page': next_page
    })

def post(request, slug):
    filepath = os.path.join(settings.BASE_DIR, 'blog', 'posts', f"{slug}.md")
    if not os.path.exists(filepath):
        raise Http404("Post not found")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            content = content.split('---', 2)[-1]  # remove front matter
    html = markdown.markdown(content)
    return render(request, 'blog/post.html', {'content': html})