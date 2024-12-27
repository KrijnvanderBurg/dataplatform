"""
File handler with a simple factory pattern.
"""

import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml


class FileHandlerBase(ABC):
    """Base class for file handlers."""

    def __init__(self, filepath: str) -> None:
        """
        Initialize the file handler.

        Args:
            filepath (str): The path to the file.
        """
        self.filepath: Path = Path(filepath)

    @abstractmethod
    def read(self) -> dict[str, Any]:
        """
        Read the file and return its contents as a dictionary.

        Returns:
            dict[str, Any]: The contents of the file.
        """
        raise NotImplementedError


class YamlFileHandler(FileHandlerBase):
    """Handles YAML files."""

    def read(self) -> dict[str, Any]:
        """
        Read the YAML file and return its contents as a dictionary.

        Returns:
            dict[str, Any]: The contents of the YAML file as a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If permission is denied for accessing the file.
            ValueError: If there is an error reading the YAML file.
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"File '{self.filepath}' not found.")

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except PermissionError as e:
            raise PermissionError(f"Permission denied for file '{self.filepath}'.") from e
        except yaml.YAMLError as e:
            raise ValueError(f"Error reading YAML file '{self.filepath}': {e}") from e


class JsonFileHandler(FileHandlerBase):
    """Handles JSON files."""

    def read(self) -> dict[str, Any]:
        """
        Read the JSON file and return its contents as a dictionary.

        Returns:
            dict[str, Any]: The contents of the JSON file as a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If permission is denied for accessing the file.
            ValueError: If there is an error decoding the JSON file.
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"File '{self.filepath}' not found.")

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except PermissionError as e:
            raise PermissionError(f"Permission denied for file '{self.filepath}'.") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON file '{self.filepath}': {e}") from e


class FileHandlerFactory:
    """Factory for creating file handlers based on file extension."""

    SUPPORTED_EXTENSIONS: dict[str, type[FileHandlerBase]] = {
        ".yml": YamlFileHandler,
        ".yaml": YamlFileHandler,
        ".json": JsonFileHandler,
    }

    @classmethod
    def create(cls, filepath: str) -> FileHandlerBase:
        """
        Create a file handler based on the file extension.

        Args:
            filepath (str): The path to the file.

        Returns:
            FileHandlerBase: An instance of the appropriate file handler.

        Raises:
            NotImplementedError: If the file extension is not supported.
        """
        _, file_extension = os.path.splitext(filepath)
        handler_class = cls.SUPPORTED_EXTENSIONS.get(file_extension)
        if handler_class is None:
            raise NotImplementedError(f"File extension '{file_extension}' is not supported.")
        return handler_class(filepath=filepath)  # type: ignore
