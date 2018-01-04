from django.shortcuts import render
from home.models import BlogArticle, Page


def home(request):
    return render(request, 'home.html', {})


def blog(request):
    all_articles = BlogArticle.objects.all()
    return render(request, 'blog.html', {"all_articles": all_articles})


def terms(request):
    return render(request, 'terms.html', {})


def personal_data_policy(request):
    return render(request, 'personal_data_policy.html', {})


def blog_article(request, num):
    article = BlogArticle.objects.get(id=num)
    return render(request, 'blog/blog_article.html', {'article': article})


def page(request):
    f = Page.objects.all()
    return render(request,'page.html', {'f':f})
