from django.shortcuts import render, get_object_or_404
from . models import Article
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django import forms
from django.core.exceptions import ValidationError


def index(request):
    articles_list = Article.objects.order_by('-pub_date')[:5]
    # latest_question_list = get_list_or_404(Question.objects.order_by('-pub_date'))[:5]
    context = {'articles_list': articles_list}
    return render(request, 'blog/index.html', context)


def display(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/display.html', {'article': article})


def edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'blog/edit.html', {'article': article})
    elif request.method == 'POST':
        article.title = request.POST['title']
        try:
            article.full_clean()
            article.save()
        except ValidationError as e:
            return render(request, 'blog/edit.html', {'error_message': str(e), 'article': article})
        return HttpResponseRedirect(reverse('blog:display', args=(article.id,)))


