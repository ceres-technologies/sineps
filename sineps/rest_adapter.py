import requests
import requests.packages
from typing import List, Dict
import logging
from json import JSONDecodeError

from .exceptions import TheRestAdapterException


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class RestAdapter:
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
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None
    ):
        full_url = self.url + endpoint
        headers = {
            "Content-Type": "application/json",
            "api-key": self._api_key,
        }

        try:
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            raise TheRestAdapterException("Request failed") from e
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise TheRestAdapterException("Bad JSON in response") from e
        if 299 >= response.status_code >= 200:
            return Result(response.status_code, message=response.reason, data=data_out)
        raise TheRestAdapterException(f"{response.status_code}: {response.reason}")

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
