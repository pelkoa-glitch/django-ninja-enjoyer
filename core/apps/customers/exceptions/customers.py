from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CustomerTokenInvalid(ServiceException):
    token: str

    @property
    def message(self):
        return 'Customer with provided token not found'
