# tests/utils/version_info_mock.py
# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportAttributeAccessIssue=false

"""Utilities for creating mock sys.version_info objects in tests."""

from typing import Any, NamedTuple


# Create a named tuple that matches sys.version_info structure
# sys.version_info is a named tuple with fields:
# major, minor, micro, releaselevel, serial


class _VersionInfo(NamedTuple):
    """Mock sys.version_info named tuple."""

    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


def create_version_info(major: int, minor: int, micro: int = 0) -> Any:
    """Create a mock sys.version_info object with major and minor attributes.

    This properly mocks sys.version_info so it can be used with attribute access
    (.major, .minor) and tuple comparison, matching the behavior of the real
    sys.version_info object (which is a named tuple).

    Args:
        major: Major version number (e.g., 3)
        minor: Minor version number (e.g., 11)
        micro: Micro version number (default: 0)

    Returns:
        A mock version_info object with .major, .minor, .micro attributes
        and tuple-like comparison support.
    """
    return _VersionInfo(
        major=major, minor=minor, micro=micro, releaselevel="final", serial=0
    )
