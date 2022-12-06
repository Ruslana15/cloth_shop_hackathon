from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

from apps.account.models import User

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.product.title}'

