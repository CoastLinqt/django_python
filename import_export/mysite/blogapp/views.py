from django.views.generic import ListView, DetailView
from .models import Article
from django.urls import reverse, reverse_lazy
from django.contrib.syndication.views import Feed


class BasedView(ListView):
    template_name = 'blogapp/article_list.html'
    model = Article
    queryset = Article.objects.filter(pub_date__isnull=False).order_by('-pub_date').defer("content").select_related('author', 'category').prefetch_related('tags')


class ArticleDetailView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:blog")

    def items(self):
        return (Article.objects.
                filter(pub_date__isnull=False)
                .order_by('-pub_date').defer("content")
                .select_related('author', 'category').prefetch_related('tags')[:5]
                )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    def item_link(self,item: Article):
        return reverse("blogapp:article", kwargs={"pk": item.pk})