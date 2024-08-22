from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass
class AuthorizeCustomerUseCase:
    customer_service: BaseCustomerService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    def authorize(self, phone: str):
        customer = self.customer_service.get_or_create(phone)
        code = self.codes_service.generate_code(customer)
        self.sender_service.send_code(customer, code)
