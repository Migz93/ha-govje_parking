"""
Data update coordinator package for govje_parking.

Package structure:
- base.py: Main coordinator class (GOVJEParkingDataUpdateCoordinator)

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from .base import GOVJEParkingDataUpdateCoordinator

__all__ = ["GOVJEParkingDataUpdateCoordinator"]
