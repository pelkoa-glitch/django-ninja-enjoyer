from functools import lru_cache
from logging import (
    getLogger,
    Logger,
)

import punq

from core.apps.customers.services.auth import (
    AuthService,
    BaseAuthService,
)
from core.apps.customers.services.codes import (
    BaseCodeService,
    DjangoCacheCodeService,
)
from core.apps.customers.services.customers import (
    BaseCustomerService,
    ORMCustomerService,
)
from core.apps.customers.services.senders import (
    BaseSenderService,
    ComposedSenderService,
    DummySenderService,
    EmailSenderService,
    PushSenderService,
)
from core.apps.products.services.products import (
    BaseProductService,
    ORMProductService,
)
from core.apps.products.services.reivews import (
    BaseReviewService,
    BaseReviewValidatorService,
    ComposerReviewValidatorService,
    ORMReviewService,
    ReviewRatingValidatorService,
    SingleReviewValidatorService,
)
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # initialize products
    container.register(BaseProductService, ORMProductService)

    # initialize customers
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(
        BaseSenderService,
        ComposedSenderService,
        sender_services=(
            DummySenderService(),
            EmailSenderService(),
            PushSenderService(),
        ),
    )
    container.register(BaseAuthService, AuthService)
    container.register(BaseReviewService, ORMReviewService)
    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)
    container.register(Logger, factory=getLogger, name='django.request')

    def build_validators() -> BaseReviewValidatorService:
        return ComposerReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService),
            ],
        )

    container.register(BaseReviewValidatorService, factory=build_validators)

    container.register(CreateReviewUseCase)

    return container
