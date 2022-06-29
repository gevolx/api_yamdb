from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from titles.models import SCORE, Title
from users.models import User


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
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
        validators=[
            MinValueValidator(1, 'Поставьте оценку от 1 до 10'),
            MaxValueValidator(10, 'Поставьте оценку от 1 до 10')
        ],
        blank=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='uniq_review')
        ]

    def __str__(self):
        return self.text


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
