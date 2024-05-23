from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CodeExeption(ServiceException):
    @property
    def message(self):
        return 'Auth code exception occured'


@dataclass(eq=False)
class CodeNotFoundExceptions(CodeExeption):
    code: str

    @property
    def message(self):
        return 'Code not found'


@dataclass(eq=False)
class CodesNotEqualException(CodeExeption):
    code: str
    cached_code: str
    customer_phone: str

    @property
    def message(self):
        return 'Codes are not equal'
