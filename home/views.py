from django.shortcuts import render, get_list_or_404, get_object_or_404
from home.models import BlogArticle, Section


def home(request):
    return render(request, 'home.html', {})


def blog(request):
    all_articles = BlogArticle.objects.all()
    return render(request, 'blog/blog.html', {"all_articles": all_articles})


def terms(request):
    return render(request, 'site_info/terms.html', {})


def personal_data_policy(request):
    return render(request, 'site_info/personal_data_policy.html', {})


def blog_article(request, num):
    article = BlogArticle.objects.get(id=num)
    return render(request, 'blog/blog_article.html', {'article': article})


def blog_sections(request):
    sections = Section.objects.all()
    return render(request, 'blog/blog_sections.html', {'sections': sections})


def blog_section(request, num):
    articles = get_list_or_404(BlogArticle, section_id=num)
    name_section = get_object_or_404(Section, id=num)
    return render(request, 'blog/blog_section.html', {'all_articles': articles,
                                                      'name_section': name_section})
