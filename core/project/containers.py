from functools import lru_cache
from logging import (
    getLogger,
    Logger,
)

from django.conf import settings

import punq
from httpx import Client

from core.apps.common.clients.elasticsearch import ElasticClient
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
from core.apps.customers.use_cases.auth.authorize import AuthorizeCustomerUseCase
from core.apps.customers.use_cases.auth.confirm_authorization import ConfirmAuthorizationCustomerUseCase
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
from core.apps.products.services.search import (
    BaseProductSearchService,
    ElasticProductSearchService,
)
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.apps.products.use_cases.search.upsert_search_data import UpsertSearchDataUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    def build_elastic_search_service() -> BaseProductSearchService:
        return ElasticProductSearchService(
            client=ElasticClient(
                http_client=Client(base_url=settings.ELASTIC_URL),
            ),
            index_name=settings.ELASTIC_PRODUCT_INDEX,
        )

    # init internal stuff
    container.register(Logger, factory=getLogger, name='django.request')

    # initialize services
    container.register(BaseProductService, ORMProductService)
    container.register(BaseReviewService, ORMReviewService)

    def build_validators() -> BaseReviewValidatorService:
        return ComposerReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService),
            ],
        )
    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)
    container.register(BaseProductSearchService, factory=build_elastic_search_service)
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
    container.register(BaseReviewValidatorService, factory=build_validators)

    # init use cases
    container.register(UpsertSearchDataUseCase)
    container.register(CreateReviewUseCase)
    container.register(AuthorizeCustomerUseCase)
    container.register(ConfirmAuthorizationCustomerUseCase)

    return container
