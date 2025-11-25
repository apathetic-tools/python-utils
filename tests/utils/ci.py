# tests/utils/ci.py

import os
from typing import TypeVar


T = TypeVar("T")


def is_ci() -> bool:
    """Check if running in a CI environment.

    Returns True if any of the following environment variables are set:
    - CI: Generic CI indicator (set by most CI systems)
    - GITHUB_ACTIONS: GitHub Actions specific
    - GIT_TAG: Indicates a tagged build
    - GITHUB_REF: GitHub Actions ref (branch/tag)
    """
    return bool(
        os.getenv("CI")
        or os.getenv("GITHUB_ACTIONS")
        or os.getenv("GIT_TAG")
        or os.getenv("GITHUB_REF")
    )


def if_ci(ci_value: T, local_value: T) -> T:
    r"""Return different values based on CI environment.

    Useful for tests that need different behavior or expectations
    in CI vs local development environments.

    Args:
        ci_value: Value to return when running in CI
        local_value: Value to return when running locally

    Returns:
        ci_value if running in CI, otherwise local_value

    Example:
        # Different regex patterns for commit hashes
        commit_pattern = if_ci(
            r"[0-9a-f]{4,}",  # CI: expect actual commit hash
            r"unknown \\(local build\\)"  # Local: expect placeholder
        )
    """
    return ci_value if is_ci() else local_value
