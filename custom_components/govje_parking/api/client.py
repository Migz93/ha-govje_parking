"""API Client for govje_parking."""

from __future__ import annotations

import asyncio
import socket
from typing import Any

import aiohttp

from custom_components.govje_parking.const import REMOTE_URL

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HomeAssistant/govje_parking)",
    "Accept": "application/json",
}


class GOVJEParkingApiClientError(Exception):
    """Base exception to indicate a general API error."""


class GOVJEParkingApiClientCommunicationError(GOVJEParkingApiClientError):
    """Exception to indicate a communication error with the API."""


class GOVJEParkingApiClientAuthenticationError(GOVJEParkingApiClientError):
    """Exception to indicate an authentication error with the API."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the API response is valid, raising on HTTP errors."""
    response.raise_for_status()


class GOVJEParkingApiClient:
    """API Client for the Government of Jersey parking data feed.

    Fetches the raw public car park availability JSON.
    No authentication is required.
    """

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialise the API client."""
        self._session = session

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch raw car park JSON from the Government of Jersey feed.

        Returns:
            Raw decoded JSON dict from the API endpoint.

        Raises:
            GOVJEParkingApiClientCommunicationError: On network, timeout, or HTTP errors.
            GOVJEParkingApiClientError: For unexpected errors.
        """
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method="get",
                    url=REMOTE_URL,
                    headers=_HEADERS,
                )
                _verify_response_or_raise(response)
                return await response.json(content_type=None)  # type: ignore[no-any-return]

        except TimeoutError as exception:
            msg = f"Timeout fetching parking data - {exception}"
            raise GOVJEParkingApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching parking data - {exception}"
            raise GOVJEParkingApiClientCommunicationError(msg) from exception
        except GOVJEParkingApiClientCommunicationError:
            raise
        except Exception as exception:
            msg = f"Unexpected error fetching parking data - {exception}"
            raise GOVJEParkingApiClientError(msg) from exception
