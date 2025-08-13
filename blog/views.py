import os
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
import markdown

import os
from django.shortcuts import render
from django.conf import settings

def index(request):
    posts_dir = os.path.join(settings.BASE_DIR, 'blog', 'posts')
    posts = sorted([f[:-3] for f in os.listdir(posts_dir) if f.endswith('.md')], reverse=True)

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

    # Determine previous and next pages
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if end < len(posts) else None

    return render(request, 'blog/index.html', {
        'posts': paginated_posts,
        'prev_page': prev_page,
        'next_page': next_page
    })

def post(request, slug):
    # Show single Markdown post
    filepath = os.path.join(settings.BASE_DIR, 'blog', 'posts', f"{slug}.md")
    if not os.path.exists(filepath):
        raise Http404("Post not found")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = markdown.markdown(f.read())
    return render(request, 'blog/post.html', {
        'content': html
    })