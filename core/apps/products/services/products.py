from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.products.entities.products import Product
from core.apps.products.exeptions.products import ProductNotFound
from core.apps.products.filters.products import ProductFilters
from core.apps.products.models.products import Product as ProductModel


class BaseProductService(ABC):
    @abstractmethod
    def get_product_list(self, filters: ProductFilters, pagination: PaginationIn) -> Iterable[Product]:
        ...

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int:
        ...

    @abstractmethod
    def get_by_id(self, product_id: int) -> int:
        ...

    @abstractmethod
    def get_all_products(self) -> Iterable[Product]:
        ...


class ORMProductService(BaseProductService):
    def _build_get_product_querry(self, filters: ProductFilters) -> Q:
        query = Q(is_visible=True)

        if filters.search is not None:
            query &= (Q(title__icontains=filters.search) | Q(description__icontains=filters.search))

        return query

    def get_product_list(self, filters: ProductFilters, pagination: PaginationIn) -> Iterable[Product]:
        query = self._build_get_product_querry(filters)
        qs = ProductModel.objects.filter(query)[pagination.offset:pagination.offset+pagination.limit]

        return [product.to_entity() for product in qs]

    def get_product_count(self, filters: ProductFilters) -> int:
        query = self._build_get_product_querry(filters)

        return ProductModel.objects.filter(query).count()

    def get_by_id(self, product_id: int) -> int:
        try:
            product_dto = ProductModel.objects.get(pk=product_id)
        except ProductModel.DoesNotExist:
            raise ProductNotFound(product_id=product_id)

        return product_dto.to_entity()

    def get_all_products(self) -> Iterable[Product]:
        query = self._build_get_product_querry(ProductFilters())
        queryset = ProductModel.objects.filter(query)

        for product in queryset:
            yield product.to_entity()
