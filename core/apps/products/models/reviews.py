from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import Review as ReviewEntity


class Review(TimedBaseModel):
    customer = models.ForeignKey(
        to='customers.Customer',
        verbose_name='Reviewer',
        related_name='product_reviews',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to='products.Product',
        verbose_name='Product',
        related_name='product_reviews',
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='User rating',
        default=1,
    )
    text = models.TextField(
        verbose_name='Review text',
        blank=True,
        default='',
    )

    @classmethod
    def from_entity(
        cls,
        review: ReviewEntity,
        product: ProductEntity,
        customer: CustomerEntity,
    ) -> 'Review':
        return cls(
            pk=review.id,
            product_id=product.id,
            customer_id=customer.id,
            text=review.text,
            rating=review.rating,
        )

    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            id=self.id,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return f'Отзыв на {self.product.title}'

    class Meta:
        verbose_name = 'Product review'
        verbose_name_plural = 'Product review'
        unique_together = (
            ('customer', 'product'),
        )
