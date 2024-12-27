"""
FileHandler strategy tests.
"""

from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from a1a_infra_base.file import FileHandlerBase, FileHandlerFactory, JsonFileHandler, YamlFileHandler


class TestYamlFileHandler:
    """Tests for YamlFileHandler class."""

    def test_read(self) -> None:
        """Test reading YAML data from a file."""
        # Arrange
        with (
            patch("builtins.open", mock_open(read_data="key: value")),
            patch.object(Path, "exists", return_value=True),
        ):
            # Act
            handler = YamlFileHandler(filepath="test.yaml")
            data = handler.read()

            # Assert
            assert data == {"key": "value"}

    def test_read__file_not_exists(self) -> None:
        """Test reading YAML file raises `FileNotFoundError` when file does not exist."""
        # Arrange
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):  # Assert
                # Act
                handler = YamlFileHandler(filepath="test.yaml")
                handler.read()

    def test_read__file_permission_error(self) -> None:
        """Test reading YAML file raises `PermissionError` when `builtins.open()` raises `PermissionError`."""
        # Arrange
        with (
            patch("builtins.open", side_effect=PermissionError),
            patch.object(Path, "exists", return_value=True),
        ):
            with pytest.raises(PermissionError):  # Assert
                # Act
                handler = YamlFileHandler(filepath="test.yaml")
                handler.read()

    def test_read__yaml_error(self) -> None:
        """Test reading YAML file raises `YAMLError` when file contains invalid YAML."""
        # Arrange
        invalid_yaml = "key: value:"  # colon `:` after value: is invalid YAML.
        with (
            patch("builtins.open", mock_open(read_data=invalid_yaml)),
            patch.object(Path, "exists", return_value=True),
        ):
            with pytest.raises(ValueError):  # Assert
                # Act
                handler = YamlFileHandler(filepath="test.yaml")
                handler.read()


class TestJsonFileHandler:
    """Tests for JsonFileHandler class."""

    def test_read(self) -> None:
        """Test reading JSON data from a file."""
        # Arrange
        with (
            patch("builtins.open", mock_open(read_data='{"key": "value"}')),
            patch.object(Path, "exists", return_value=True),
        ):
            # Act
            handler = JsonFileHandler(filepath="test.json")
            data = handler.read()

            # Assert
            assert data == {"key": "value"}

    def test_read__file_not_exists(self) -> None:
        """Test reading JSON file raises `FileNotFoundError` when file does not exist."""
        # Arrange
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):  # Assert
                # Act
                handler = JsonFileHandler(filepath="test.json")
                handler.read()

    def test_read__file_permission_error(self) -> None:
        """Test reading JSON file raises `PermissionError` when `builtins.open()` raises `PermissionError`."""
        # Arrange
        with (
            patch("builtins.open", side_effect=PermissionError),
            patch.object(Path, "exists", return_value=True),
        ):
            with pytest.raises(PermissionError):  # Assert
                # Act
                handler = JsonFileHandler(filepath="test.json")
                handler.read()

    def test_read__json_decode_error(self) -> None:
        """Test reading JSON file raises `ValueError` when file contains invalid JSON."""
        # Arrange
        invalid_json = '{"name": "John" "age": 30}'  # Missing comma makes it invalid JSON.
        with (
            patch("builtins.open", mock_open(read_data=invalid_json)),
            patch.object(Path, "exists", return_value=True),
        ):
            with pytest.raises(ValueError):  # Assert
                # Act
                handler = JsonFileHandler(filepath="test.json")
                handler.read()


class TestFileHandlerFactory:
    """Tests for FileHandlerFactory class."""

    @pytest.mark.parametrize(
        "filepath, expected_handler",
        [
            ("test.yml", YamlFileHandler),
            ("test.yaml", YamlFileHandler),
            ("test.json", JsonFileHandler),
        ],
    )
    def test_create(self, filepath: str, expected_handler: type[FileHandlerBase]) -> None:
        """
        Test `create` returns the correct handler for given file extension.

        Args:
            filepath (str): The file path to create the handler for.
            expected_handler (type): The expected handler type.
        """
        # Act
        handler = FileHandlerFactory.create(filepath=filepath)

        # Assert
        assert isinstance(handler, expected_handler)

    def test_create__unsupported_extension__raises_not_implemented_error(self) -> None:
        """Test `create` raises `NotImplementedError` for unsupported file extension."""
        with pytest.raises(NotImplementedError):  # Assert
            FileHandlerFactory.create("path/fail.testfile")  # Act
