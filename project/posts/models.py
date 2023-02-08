from django.db import models


class Post(models.Model):
    """
    Модель поста
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Текст поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Comment(models.Model):
    """
    Модель комментария. Привязывается к определенному посту.
    """
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')

    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
