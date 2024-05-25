import random
from abc import (
    ABC,
    abstractmethod,
)

from django.core.cache import cache

from core.apps.customers.entities.customers import Customer
from core.apps.customers.exceptions.codes import (
    CodeNotFoundExceptions,
    CodesNotEqualException,
)


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, customer: Customer) -> str:
        ...

    @abstractmethod
    def validate_code(self, customer: Customer) -> None:
        ...


class DjangoCacheCodeService(BaseCodeService):
    def generate_code(self, customer: Customer) -> str:
        code = str(random.randint(100000, 999999)) # noqa
        cache.set(customer.phone, code)
        return code

    def validate_code(self, code: str, customer: Customer) -> None:
        cached_code = cache.get(customer.phone)

        if cached_code is None:
            raise CodeNotFoundExceptions(code=code)

        if cached_code != code:
            raise CodesNotEqualException(
                code=code,
                cached_code=cached_code,
                customer_phone=customer.phone,
            )
        cache.delete(customer.phone)
