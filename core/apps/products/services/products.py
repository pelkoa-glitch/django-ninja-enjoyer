from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.entities.products import Product
from core.apps.products.models.products import Product as ProductModel


class BaseProductService(ABC):
    @abstractmethod
    def get_product_list(self, filters: ProductFilters, pagination: PaginationIn) -> Iterable[Product]:
        ...

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int:
        ...


class ORMProductService(BaseProductService):
    def _builq_get_product_querry(self, filters: ProductFilters) -> Q:
        query = Q(is_visible=True)

        if filters.search is not None:
            query &= (Q(title__icontains=filters.search) | Q(description__icontains=filters.search))

        return query

    def get_product_list(self, filters: ProductFilters, pagination: PaginationIn) -> Iterable[Product]:
        query = self._builq_get_product_querry(filters)
        qs = ProductModel.objects.filter(query)[pagination.offset:pagination.offset+pagination.limit]

        return [product.to_entity() for product in qs]

    def get_product_count(self, filters: ProductFilters) -> int:
        query = self._builq_get_product_querry(filters)

        return ProductModel.objects.filter(query).count()
