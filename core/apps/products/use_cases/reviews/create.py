from dataclasses import dataclass
from logging import Logger

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.services.products import BaseProductService
from core.apps.products.services.reivews import (
    BaseReviewService,
    BaseReviewValidatorService,
)


@dataclass
class CreateReviewUseCase:
    review_servise: BaseReviewService
    customer_service: BaseCustomerService
    product_service: BaseProductService
    validator_service: BaseReviewValidatorService
    logger: Logger

    def execute(
        self,
        product_id: int,
        customer_token: str,
        review: ReviewEntity,
    ) -> ReviewEntity:
        customer = self.customer_service.get_by_token(token=customer_token)
        product = self.product_service.get_by_id(product_id=product_id)

        self.validator_service.validate(review=review, customer=customer, product=product)
        saved_review = self.review_servise.save_review(product=product, customer=customer, review=review)

        return saved_review
