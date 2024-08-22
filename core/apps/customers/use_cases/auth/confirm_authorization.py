from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass
class ConfirmAuthorizationCustomerUseCase:
    customer_service: BaseCustomerService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    def confirm(self, code: str, phone: str):
        customer = self.customer_service.get(phone)
        self.codes_service.validate_code(code, customer)
        return self.customer_service.generate_token(customer)
