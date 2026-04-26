"""API package for govje_parking.

Exception hierarchy:
    GOVJEParkingApiClientError (base)
    ├── GOVJEParkingApiClientCommunicationError (network/timeout/HTTP errors)
    └── GOVJEParkingApiClientAuthenticationError (401/403 — unused for this integration)

Coordinator exception mapping:
    ApiClientCommunicationError → UpdateFailed (auto-retry)
    ApiClientError              → UpdateFailed (auto-retry)
"""

from .client import (
    GOVJEParkingApiClient,
    GOVJEParkingApiClientAuthenticationError,
    GOVJEParkingApiClientCommunicationError,
    GOVJEParkingApiClientError,
)

__all__ = [
    "GOVJEParkingApiClient",
    "GOVJEParkingApiClientAuthenticationError",
    "GOVJEParkingApiClientCommunicationError",
    "GOVJEParkingApiClientError",
]
