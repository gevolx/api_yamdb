from django.db import models

from users.models import User
from titles.models import Title, SCORE


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    pub_date = models.DateField(
        auto_now_add=True
    )
    text = models.TextField(
        'Текст Отзыва'
    )
    score = models.IntegerField(
        'Оценка отзыва',
        choices=SCORE,
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='uniq_review')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateField(
        auto_now_add=True
    )
    text = models.TextField(
        'Текст комментария'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
