from rest_framework.serializers import ModelSerializer, SerializerMethodField, DateTimeField

from .models import Post, Comment


class CommentsListSerializer(ModelSerializer):
    class Meta: 
        model = Comment
        fields = ('pk', 'text', 'post')


class CommentSerializer(ModelSerializer):
    class Meta: 
        model = Comment
        fields = ('pk', 'text')


class PostsListSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    comment = SerializerMethodField()

    def get_comment(self, obj):
        comment = obj.comments.first()
        if comment:
            return CommentSerializer(comment).data
        return None

    class Meta: 
        model = Post
        fields = ('pk', 'title', 'text', 'created_at', 'comment')


class PostSerializer(ModelSerializer):
    created_at = DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    comments = CommentSerializer(many=True)

    class Meta: 
        model = Post
        fields = ('pk', 'title', 'text', 'created_at', 'views', 'comments')

