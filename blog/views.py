import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import EmailVerification
from .forms import EmailForm, CodeForm
import uuid
from django.core.mail import send_mail
import datetime
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

    for filename in files:
        filepath = os.path.join(posts_dir, filename)
        meta = parse_front_matter(filepath)
        slug = filename[:-3]

        # Get date from YAML front matter
        date_value = meta.get('date', '1900-01-01')

        # Handle if date is a datetime.date object or a string
        if isinstance(date_value, datetime.date):
            date_obj = datetime.datetime.combine(date_value, datetime.datetime.min.time())
        else:
            try:
                date_obj = datetime.datetime.strptime(date_value, "%Y-%m-%d")
            except ValueError:
                date_obj = datetime.datetime.min

        posts.append({
            'slug': slug,
            'title': meta.get('title', slug),
            'thumbnail': meta.get('thumbnail', '/static/images/default.jpg'),
            'date': date_value,
            'date_obj': date_obj
        })

    # Sort by date descending (newest first)
    posts.sort(key=lambda p: p['date_obj'], reverse=True)

    # Pagination
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

def search(request):
    query = request.GET.get("q")
    posts_dir = os.path.join(settings.BASE_DIR, 'blog', 'posts')

    if query:
        files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
        matches = []

        for filename in files:
            filepath = os.path.join(posts_dir, filename)
            meta = parse_front_matter(filepath)
            title = meta.get('title', filename[:-3])

            # Match in title (case-insensitive)
            if query.lower() in title.lower():
                matches.append({
                    'slug': filename[:-3],
                    'title': title,
                    'thumbnail': meta.get('thumbnail', '/static/images/default.jpg'),
                    'date': meta.get('date', 'Unknown Date')
                })

        return render(request, 'blog/search.html', {
            'query': query,
            'matches': matches
        })
    else:
        return redirect("index")
    
def post(request, slug):
    # Load Markdown content as usual
    filepath = os.path.join(settings.BASE_DIR, 'blog', 'posts', f"{slug}.md")
    if not os.path.exists(filepath):
        raise Http404("Post not found")

    # Check if post is restricted (using front matter)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().split('---')
        meta = {}
        if len(lines) >= 3:
            meta = yaml.safe_load(lines[1])
        restricted = meta.get('restricted', False)

    # If restricted, check session for verified email
    if restricted and not request.session.get(f'verified_{slug}', False):

        if request.method == "POST":
            # Handle email submission
            if "email_submit" in request.POST:
                form = EmailForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    code = str(uuid.uuid4()).replace("-", "")[:6]  # 6-char code
                    EmailVerification.objects.create(email=email, code=code)

                    # Send code by email
                    send_mail(
                        "Your verification code",
                        f"Use this code to access the post: {code}",
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    request.session['email_for_code'] = email
                    form = CodeForm()
                    return render(request, 'blog/verify.html', {
                        'form': form,
                        'form_type': 'code'
                    })

                # Render form with errors
                return render(request, 'blog/verify.html', {
                    'form': form,
                    'form_type': 'email'
                })

            # Handle code submission
            elif "code_submit" in request.POST:
                form = CodeForm(request.POST)
                if form.is_valid():
                    code_input = form.cleaned_data['code']
                    email = request.session.get('email_for_code')
                    try:
                        verification = EmailVerification.objects.get(email=email, code=code_input, used=False)
                        if verification.is_expired():
                            verification.used = True
                            verification.save()
                            return render(request, 'blog/verify.html', {
                                'form': CodeForm(),
                                'form_type': 'code',
                                'error': 'Code expired'
                            })
                        verification.used = True
                        verification.save()
                        request.session[f'verified_{slug}'] = True
                        return redirect(request.path)
                    except EmailVerification.DoesNotExist:
                        return render(request, 'blog/verify.html', {
                            'form': CodeForm(),
                            'form_type': 'code',
                            'error': 'Invalid code'
                        })

                # Render form with errors
                return render(request, 'blog/verify.html', {
                    'form': form,
                    'form_type': 'code'
                })

        # GET request — show email form
        form = EmailForm()
        return render(request, 'blog/verify.html', {
            'form': form,
            'form_type': 'email'
        })

    # If not restricted or already verified, show post
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            content = content.split('---', 2)[-1]  # remove front matter

    html = markdown.markdown(
        content,
        extensions=['extra', 'codehilite', 'toc'],
        output_format='html5'
    )

    return render(request, 'blog/post.html', {'content': html})

def blogview(request):
    posts_dir = os.path.join(settings.BASE_DIR, 'blog', 'posts')
    files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
    posts = []

    for filename in files:
        filepath = os.path.join(posts_dir, filename)
        meta = parse_front_matter(filepath)
        slug = filename[:-3]

        # Get date from YAML front matter
        date_value = meta.get('date', '1900-01-01')

        # Handle if date is a datetime.date object or a string
        if isinstance(date_value, datetime.date):
            date_obj = datetime.datetime.combine(date_value, datetime.datetime.min.time())
        else:
            try:
                date_obj = datetime.datetime.strptime(date_value, "%Y-%m-%d")
            except ValueError:
                date_obj = datetime.datetime.min

        posts.append({
            'slug': slug,
            'title': meta.get('title', slug),
            'thumbnail': meta.get('thumbnail', '/static/images/default.jpg'),
            'date': date_value,
            'date_obj': date_obj
        })

    # Sort by date descending (newest first)
    posts.sort(key=lambda p: p['date_obj'], reverse=True)

    # Pagination
    per_page = 10
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

    return render(request, 'blogview.html', {
        'posts': paginated_posts,
        'prev_page': prev_page,
        'next_page': next_page
    })