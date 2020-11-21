from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from common_app.models import Article


def user_is_article_author_or_admin(view):
    @wraps(view)
    def wrap(request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        if article.user == request.user.profile or request.user.is_superuser:
            return view(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorised')

    return wrap
