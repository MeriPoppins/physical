from rest_framework.viewsets import ModelViewSet
from django.db.models import F, Prefetch

from .models import Post, Comment
from .serializers import CommentsListSerializer, PostsListSerializer, PostSerializer


class CommentsViewSet(ModelViewSet):
    """
    Вьюха для отображения списка комментарий
    """

    queryset = Comment.objects.all()
    serializer_class = CommentsListSerializer

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


class PostsViewSet(ModelViewSet):
    """
    Вьюха для отображения постов
    """

    comments_queryset = Comment.objects.order_by("post_id", "-id").distinct(
        "post_id",
    )
    queryset = Post.objects.prefetch_related(
        Prefetch("comments", queryset=comments_queryset)
    )

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределен метод для увеличения счетчика просмотров
        """
        Post.objects.filter(pk=kwargs["pk"]).update(views=F("views") + 1)
        response = super().retrieve(request, *args, **kwargs)
        return response

    def get_serializer_class(self):
        if self.action in ["list"]:
            return PostsListSerializer

        return PostSerializer
