import json
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, Comment
from posts.serializers import (
    CommentsListSerializer,
    PostSerializer,
    PostsListSerializer,
)


class CommentsListApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title="post", text="text", created_at=datetime.now(), views=0
        )
        self.comment = Comment.objects.create(
            text="text", created_at=datetime.now(), post=self.post
        )

    def test_get_list(self):
        url = reverse("comment-list")
        response = self.client.get(url)
        serializer_data = CommentsListSerializer([self.comment], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse("comment-detail", args=(self.comment.id,))
        response = self.client.get(url)

        serializer_data = CommentsListSerializer(self.comment).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(1, Comment.objects.all().count())
        url = reverse("comment-list")
        data = {
            "id": 2,
            "text": "text2",
            "created_at": str(datetime.now()),
            "post": self.post.id,
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Comment.objects.all().count())

    def test_update(self):
        url = reverse("comment-detail", args=(self.comment.id,))
        data = {"text": "text text"}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.comment.refresh_from_db()
        self.assertEqual("text text", self.comment.text)

    def test_delete(self):
        self.assertEqual(1, Comment.objects.all().count())
        url = reverse("comment-detail", args=(self.comment.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Comment.objects.all().count())


class PostsSerializerApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title="post", text="text", created_at=datetime.now(), views=0
        )
        self.comment = Comment.objects.create(
            text="text", created_at=datetime.now(), post=self.post
        )

    def test_get_list(self):
        url = reverse("post-list")
        response = self.client.get(url)
        serializer_data = PostsListSerializer([self.post], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse("post-detail", args=(self.post.id,))
        response = self.client.get(url)

        serializer_data = PostSerializer(self.post).data
        serializer_data["views"] += 1

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
