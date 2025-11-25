# src/apathetic_utils/ci.py
"""CI environment detection utilities."""

from __future__ import annotations

import os
from typing import ClassVar


class ApatheticUtils_Internal_CI:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides CI environment detection functionality.

    This class contains utilities for detecting CI environments.
    When mixed into apathetic_utils, it provides CI detection methods.
    """

    # CI environment variable names that indicate CI environment
    CI_ENV_VARS: ClassVar[tuple[str, ...]] = (
        "CI",
        "GITHUB_ACTIONS",
        "GIT_TAG",
        "GITHUB_REF",
    )

    @staticmethod
    def is_ci() -> bool:
        """Check if running in a CI environment.

        Returns True if any of the following environment variables are set:
        - CI: Generic CI indicator (set by most CI systems)
        - GITHUB_ACTIONS: GitHub Actions specific
        - GIT_TAG: Indicates a tagged build
        - GITHUB_REF: GitHub Actions ref (branch/tag)

        Returns:
            True if running in CI, False otherwise
        """
        return bool(
            any(os.getenv(var) for var in ApatheticUtils_Internal_CI.CI_ENV_VARS)
        )
