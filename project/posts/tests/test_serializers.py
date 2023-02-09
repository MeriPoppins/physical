from django.test import TestCase
from datetime import datetime

from posts.models import Comment, Post
from posts.serializers import (
    CommentsListSerializer,
    CommentSerializer,
    PostsListSerializer,
    PostSerializer,
)


class CommentsListSerializersTestCase(TestCase):
    def test_ok(self):
        post = Post.objects.create(
            title="post", text="text", created_at=datetime.now(), views=0
        )
        comment = Comment.objects.create(
            text="text", created_at=datetime.now(), post=post
        )
        data = CommentsListSerializer([comment], many=True).data
        expected_data = [
            {
                "pk": comment.id,
                "text": "text",
                "post": post.id,
            }
        ]
        self.assertEqual(expected_data, data)


class CommentSerializersTestCase(TestCase):
    def test_ok(self):
        post = Post.objects.create(
            title="post", text="text", created_at=datetime.now(), views=0
        )
        comment = Comment.objects.create(
            text="text", created_at=datetime.now(), post=post
        )
        data = CommentSerializer([comment], many=True).data
        expected_data = [{"pk": comment.id, "text": "text"}]
        self.assertEqual(expected_data, data)


class PostsListSerializerTestCase(TestCase):
    def test_ok(self):
        post = Post.objects.create(
            title="post", text="text", created_at=datetime.now(), views=0
        )
        comment = Comment.objects.create(
            text="text", created_at=datetime.now(), post=post
        )
        data = PostsListSerializer([post], many=True).data
        expected_data = [
            {
                "pk": post.id,
                "title": "post",
                "text": "text",
                "created_at": datetime.strftime(post.created_at, "%Y-%m-%dT%H:%M:%S"),
                "comment": {"pk": comment.pk, "text": "text"},
            }
        ]
        self.assertEqual(expected_data, data)


class PostSerializerTestCase(TestCase):
    def test_ok(self):
        post = Post.objects.create(
            title="post", text="text", created_at=datetime.now(), views=0
        )
        comment = Comment.objects.create(
            text="text", created_at=datetime.now(), post=post
        )
        data = PostSerializer(post).data
        expected_data = {
            "pk": post.id,
            "title": "post",
            "text": "text",
            "created_at": datetime.strftime(post.created_at, "%Y-%m-%dT%H:%M:%S"),
            "views": 0,
            "comments": [{"pk": comment.pk, "text": "text"}],
        }
        self.assertEqual(expected_data, data)
