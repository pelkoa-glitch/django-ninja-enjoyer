from uuid import uuid4

from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities.customers import Customer


class Customer(TimedBaseModel):
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        unique=True,
    )
    token = models.CharField(
        verbose_name='Токен пользователя',
        max_length=255,
        default=uuid4,
        unique=True,
    )

    def to_entity(self) -> Customer:
        return Customer(phone=self.phone, created_at=self.created_at, id=self.pk)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
