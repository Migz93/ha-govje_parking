"""
API package for govje_parking.

Architecture:
    Three-layer data flow: Entities → Coordinator → API Client.
    Only the coordinator should call the API client. Entities must never
    import or call the API client directly.

Exception hierarchy:
    GOVJEParkingApiClientError (base)
    └── GOVJEParkingApiClientCommunicationError (network/timeout)

Coordinator exception mapping:
    ApiClientCommunicationError → UpdateFailed (auto-retry)
    ApiClientError              → UpdateFailed (auto-retry)
"""

from .client import GOVJEParkingApiClient, GOVJEParkingApiClientCommunicationError, GOVJEParkingApiClientError

__all__ = [
    "GOVJEParkingApiClient",
    "GOVJEParkingApiClientCommunicationError",
    "GOVJEParkingApiClientError",
]
