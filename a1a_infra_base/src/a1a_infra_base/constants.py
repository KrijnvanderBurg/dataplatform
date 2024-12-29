"""
Module constants

This module defines constants for Azure locations and resources using Enums.

Classes:
    AzureLocation: Enum representing Azure locations with their full names and abbreviations.
    AzureResource: Enum representing Azure resources with their full names and abbreviations.
"""

from enum import Enum
from typing import Self


class AzureLocation(Enum):
    """
    Enum representing Azure locations with their full names and abbreviations.
    """

    WEST_EUROPE = ("west europe", "we")
    GERMANY_WEST_CENTRAL = ("germany west central", "gwc")

    def __init__(self, full_name: str, abbr: str) -> None:
        """
        Initialize the AzureLocation enum with full name and abbreviation.

        Args:
            full_name (str): The full name of the Azure location.
            abbr (str): The abbreviation of the Azure location.
        """
        self._full_name = full_name
        self._abbr = abbr

    @property
    def full_name(self) -> str:
        """
        Get the full name of the Azure location.

        Returns:
            str: The full name of the Azure location.
        """
        return self._full_name

    @property
    def abbr(self) -> str:
        """
        Get the abbreviation of the Azure location.

        Returns:
            str: The abbreviation of the Azure location.
        """
        return self._abbr

    @classmethod
    def from_full_name(cls, full_name: str) -> Self:
        """
        Get the AzureLocation enum member from the full name.

        Args:
            full_name (str): The full name of the Azure location.

        Returns:
            AzureLocation: The corresponding AzureLocation enum member.

        Raises:
            ValueError: If no matching AzureLocation is found.
        """
        location = next((loc for loc in cls if loc.full_name == full_name), None)
        if location is None:
            raise ValueError(f"No AzureLocation with full name '{full_name}' found.")
        return location


class AzureResource(Enum):
    """
    Enum representing Azure resources with their full names and abbreviations.
    """

    RESOURCE_GROUP = "resource_group", "rg"
    STORAGE_ACCOUNT = "storage_account", "st"
    MANAGEMENT_LOCK = "management_lock", "lock"

    def __init__(self, full_name: str, abbr: str) -> None:
        """
        Initialize the AzureResource enum with full name and abbreviation.

        Args:
            full_name (str): The full name of the Azure resource.
            abbr (str): The abbreviation of the Azure resource.
        """
        self._full_name = full_name
        self._abbr = abbr

    @property
    def full_name(self) -> str:
        """
        Get the full name of the Azure resource.

        Returns:
            str: The full name of the Azure resource.
        """
        return self._full_name

    @property
    def abbr(self) -> str:
        """
        Get the abbreviation of the Azure resource.

        Returns:
            str: The abbreviation of the Azure resource.
        """
        return self._abbr

    @classmethod
    def from_full_name(cls, full_name: str) -> Self:
        """
        Get the AzureResource enum member from the full name.

        Args:
            full_name (str): The full name of the Azure resource.

        Returns:
            AzureResource: The corresponding AzureResource enum member.

        Raises:
            ValueError: If no matching AzureResource is found.
        """
        location = next((loc for loc in cls if loc.full_name == full_name), None)
        if location is None:
            raise ValueError(f"No AzureResource with full name '{full_name}' found.")
        return location
