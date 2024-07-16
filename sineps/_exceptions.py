class SinepsException(Exception):
    pass


class IntentRouterException(SinepsException):
    pass


class InvalidIntentRouterFormatException(IntentRouterException):
    pass


class FilterExtractorException(SinepsException):
    pass


class InvalidFilterExtractorFormatException(FilterExtractorException):
    pass


class SinepsClientException(Exception):
    pass


class SinepsAsyncClientException(Exception):
    pass


class RestAdapterException(Exception):
    pass


class AsyncRestAdapterException(Exception):
    pass
