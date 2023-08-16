from django.db import models
from users.models import User


class Orders(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=250)
    address = models.CharField(max_length=250)
    basket_history = models.JSONField(default=dict)
    create = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = 'заказы'
        verbose_name = 'заказ'
