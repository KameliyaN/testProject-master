from django import forms

from common_app.models import Article, Comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea())


    class Meta:
        model = Article
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'article')
