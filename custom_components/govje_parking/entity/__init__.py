"""
Entity package for govje_parking.

Architecture:
    All platform entities inherit from (PlatformEntity, GOVJEParkingEntity).
    MRO order matters — platform-specific class first, then the integration base.
    Entities read data from coordinator.data and NEVER call the API client directly.
    Unique IDs follow the pattern: {entry_id}_{description.key}

See entity/base.py for the GOVJEParkingEntity base class.
"""

from .base import GOVJEParkingEntity

__all__ = ["GOVJEParkingEntity"]
