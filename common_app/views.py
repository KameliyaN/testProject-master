from datetime import date

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from accounts.models import Profile
from common_app.decorators import user_is_article_author_or_admin
from common_app.forms import ArticleForm
from common_app.models import Article


def homepage(request):
    # params = {
    #     'token': 'sgfnw2wtulfkxlbid2dg',
    #     'currency': 'EUR/USD USD/JPY GBP/USD AUD/USD USD/CAD'
    # }
    # api_result = requests.get('https://currencydatafeed.com/api/data.php', params)
    #
    # api_response = api_result.json()
    # currencies = api_response['currency']

    context = {
        'articles': Article.objects.all(),
        # 'currencies': currencies

    }

    return render(request, 'common_app/index.html', context)


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "common_app/article_create.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        # profile = Profile.objects.get(user_id=self.request.user.id)
        article.user = self.request.user.profile
        article.save()
        return redirect('home')


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    context_object_name = 'article'
    template_name = "common_app/article_view.html"


@method_decorator(user_is_article_author_or_admin, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "common_app/article_edit.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        article.save()
        return redirect('view article', article.id)


@method_decorator(user_is_article_author_or_admin, name='dispatch')
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    context_object_name = 'article'


class ArticlesUserAllView(LoginRequiredMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = "common_app/view_all_user_articles.html"

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Article.objects.filter(user_id=pk)
        # queryset = super(ArticlesUserAllView, self).get_queryset()
        # return queryset.filter(user_id=self.kwargs['pk'])
