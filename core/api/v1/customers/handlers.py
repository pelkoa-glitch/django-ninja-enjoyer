from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    AuthInSchema,
    AuthOutSchema,
    TokenInSchema,
    TokenOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.customers.use_cases.auth.authorize import AuthorizeCustomerUseCase
from core.apps.customers.use_cases.auth.confirm_authorization import ConfirmAuthorizationCustomerUseCase
from core.project.containers import get_container


router = Router(tags=['Customers'])


@router.post('auth', response=ApiResponse[AuthOutSchema], operation_id='authorize')
def auth_handler(request: HttpRequest, schema: AuthInSchema) -> ApiResponse[AuthOutSchema]:
    container = get_container()

    use_case: AuthorizeCustomerUseCase = container.resolve(AuthorizeCustomerUseCase)

    use_case.authorize(schema.phone)

    return ApiResponse(
        data=AuthOutSchema(
            message=f'Code is sent to: {schema.phone}',
        ),
    )


@router.post('confirm', response=ApiResponse[TokenOutSchema], operation_id='confirmCode')
def get_token_handler(request: HttpRequest, schema: TokenInSchema) -> ApiResponse[TokenOutSchema]:
    container = get_container()

    use_case: ConfirmAuthorizationCustomerUseCase = container.resolve(ConfirmAuthorizationCustomerUseCase)

    try:
        token = use_case.confirm(schema.code, schema.phone)
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        ) from exception

    return ApiResponse(data=TokenOutSchema(token=token))
