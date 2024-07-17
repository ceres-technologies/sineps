class APIError(Exception):
    pass


class IntentRouterError(APIError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidIntentRouterFormatError(IntentRouterError):
    pass


class FilterExtractorError(APIError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidFilterExtractorFormatError(FilterExtractorError):
    pass


class APIStatusError(APIError):
    def __init__(self, text: str, status_code: int, message: str):
        super().__init__(text)
        self.status_code = status_code
        self.message = message


class APIConnectionError(APIError):
    pass


class RestAdapterError(APIError):
    pass


class InternalServerError(APIStatusError):
    pass


class BadRequestError(APIStatusError):
    pass


class TooManyRequestsError(APIStatusError):
    pass


class UnauthorizedAPIKeyError(APIStatusError):
    pass


class PaymentRequiredError(APIStatusError):
    pass
