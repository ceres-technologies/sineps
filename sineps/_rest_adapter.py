import requests
import aiohttp
import requests.packages
from typing import List, Dict
import logging
from json import JSONDecodeError

from ._exceptions import (
    RestAdapterError,
    InternalServerError,
    BadRequestError,
    TooManyRequestsError,
    UnauthorizedAPIKeyError,
    PaymentRequiredError,
)


from ._utils import handle_error_message


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class BaseRestAdapter:
    def __init__(
        self,
        hostname: str,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"https://{hostname}/{ver}"
        self._api_key = api_key
        self._ssl_verify = ssl_verify

    def _define_exception_class(self, exception_class, base_exception_class):
        if exception_class:
            return exception_class
        return base_exception_class

    def _build_log_lines(self, http_method: str, endpoint: str, ep_params: Dict):
        full_url = self.url + endpoint
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )
        return full_url, log_line_pre, log_line_post

    def _log_and_raise_exception(
        self, log_line_post, success, status_code, message, exception
    ):
        log_line = log_line_post.format(success, status_code, message)
        if success:
            self._logger.debug(msg=log_line)
        else:
            self._logger.debug(msg=log_line)

            if status_code == 400:
                raise BadRequestError(
                    f"{status_code} - {message}",
                    status_code=status_code,
                    message=message,
                )
            elif status_code == 401:
                raise UnauthorizedAPIKeyError(
                    f"{status_code} - {message}",
                    status_code=status_code,
                    message=message,
                )
            elif status_code == 402:
                raise PaymentRequiredError(
                    f"{status_code} - {message}",
                    status_code=status_code,
                    message=message,
                )
            elif status_code == 429:
                raise TooManyRequestsError(
                    f"{status_code} - {message}",
                    status_code=status_code,
                    message=message,
                )
            elif status_code == 500:
                raise InternalServerError(
                    f"{status_code} - {message}",
                    status_code=status_code,
                    message=message,
                )
            raise exception


class RestAdapter(BaseRestAdapter):
    def __init__(
        self, hostname, api_key, ver, ssl_verify, logger, exception_class=None
    ):
        super().__init__(hostname, api_key, ver, ssl_verify, logger)
        self._exception_class = self._define_exception_class(
            exception_class, RestAdapterError
        )

    def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None
    ):
        full_url, log_line_pre, log_line_post = self._build_log_lines(
            http_method, endpoint, ep_params
        )
        headers = {
            "Content-Type": "application/json",
            "api-key": self._api_key,
        }

        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise self._exception_class("Request failed") from e

        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise self._exception_class("Bad JSON in response") from e

        is_success = 299 >= response.status_code >= 200
        message = handle_error_message(is_success, data_out)
        self._log_and_raise_exception(
            log_line_post,
            is_success,
            response.status_code,
            message,
            self._exception_class,
        )

        return Result(response.status_code, message=message, data=data_out)

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )

    def delete(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        return self._do(
            http_method="DELETE", endpoint=endpoint, ep_params=ep_params, data=data
        )


class AsyncRestAdapter(BaseRestAdapter):

    def __init__(
        self, hostname, api_key, ver, ssl_verify, logger, exception_class=None
    ):
        super().__init__(hostname, api_key, ver, ssl_verify, logger)
        self._exception_class = self._define_exception_class(
            exception_class, RestAdapterError
        )

    async def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None
    ):
        full_url, log_line_pre, log_line_post = self._build_log_lines(
            http_method, endpoint, ep_params
        )
        headers = {
            "Content-Type": "application/json",
            "api-key": self._api_key,
        }

        try:
            self._logger.debug(msg=log_line_pre)
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=http_method,
                    url=full_url,
                    ssl=self._ssl_verify,
                    headers=headers,
                    params=ep_params,
                    json=data,
                ) as response:
                    try:
                        data_out = await response.json()
                    except (ValueError, JSONDecodeError) as e:
                        self._logger.error(msg=log_line_post.format(False, None, e))
                        raise self._exception_class("Bad JSON in response") from e

                    is_success = 299 >= response.status >= 200
                    message = handle_error_message(is_success, data_out)
                    self._log_and_raise_exception(
                        log_line_post,
                        is_success,
                        response.status,
                        message,
                        self._exception_class(f"{response.status} - {message}"),
                    )

                    return Result(response.status, message=message, data=data_out)
        except aiohttp.ClientError as e:
            self._logger.error(msg=(str(e)))
            raise self._exception_class("Request failed") from e

    async def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return await self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    async def post(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        return await self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )

    async def delete(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        return await self._do(
            http_method="DELETE", endpoint=endpoint, ep_params=ep_params, data=data
        )
