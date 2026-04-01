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


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the API response is valid, raising on HTTP errors."""
    response.raise_for_status()


class GOVJEParkingApiClient:
    """API Client for the Government of Jersey parking data feed.

    Fetches and parses the public car park availability JSON.
    No authentication is required.

    Attributes:
        _session: The aiohttp ClientSession for making requests.
    """

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialise the API client.

        Args:
            session: The aiohttp ClientSession to use for requests.
        """
        self._session = session

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch current car park data from the Government of Jersey feed.

        Returns:
            A dict with keys:
              - "car_parks": dict mapping car park name to its data dict
                  (includes "free_spaces" plus all extra API fields)
              - "timestamp": ISO timestamp string from the feed, or None

        Raises:
            GOVJEParkingApiClientCommunicationError: On network, timeout, or HTTP errors.
            GOVJEParkingApiClientError: For unexpected errors.
        """
        return await self._api_wrapper(method="get", url=REMOTE_URL)

    async def _api_wrapper(
        self,
        method: str,
        url: str,
    ) -> dict[str, Any]:
        """Make an HTTP request and parse the parking JSON response.

        Args:
            method: The HTTP method.
            url: The URL to request.

        Returns:
            Parsed and structured parking data dict.

        Raises:
            GOVJEParkingApiClientCommunicationError: On network/timeout/HTTP errors.
            GOVJEParkingApiClientError: For unexpected errors.
        """
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=_HEADERS,
                )
                _verify_response_or_raise(response)
                raw = await response.json(content_type=None)
                return self._parse(raw)

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

    @staticmethod
    def _parse(raw: dict[str, Any]) -> dict[str, Any]:
        """Parse the raw API response into structured data.

        Args:
            raw: The decoded JSON response from the API.

        Returns:
            Dict with "car_parks" (open parks keyed by name) and "timestamp".
        """
        car_parks: dict[str, dict[str, Any]] = {}
        timestamp: str | None = None

        carpark_data = raw.get("carparkData", {})

        if "Timestamp" in carpark_data:
            timestamp = carpark_data["Timestamp"]

        jersey_data = carpark_data.get("Jersey", {})
        for carpark in jersey_data.get("carpark", []):
            name = carpark.get("name")
            if not name:
                continue
            if not carpark.get("carparkOpen"):
                continue
            try:
                free_spaces = int(carpark["spaces"])
            except (KeyError, TypeError, ValueError):
                continue

            car_parks[name] = {
                "free_spaces": free_spaces,
                **{field: value for field, value in carpark.items() if field != "spaces"},
            }

        return {"car_parks": car_parks, "timestamp": timestamp}
