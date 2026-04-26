"""String helper utilities for govje_parking."""

from __future__ import annotations

import re


def slugify_name(name: str) -> str:
    """Convert a car park name to a stable slug for use in entity keys/unique IDs.

    Example:
        >>> slugify_name("Sand Street")
        'sand_street'
    """
    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[-\s]+", "_", slug)
    return slug.strip("_")
