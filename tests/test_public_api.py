"""Tests for the public API surface of azure-functions-doctor."""

import azure_functions_doctor  # pyright: ignore[reportMissingImports]


class TestAPISurface:
    """Verify __version__ is exported and package is importable."""

    def test_version_is_importable(self) -> None:
        assert hasattr(azure_functions_doctor, "__version__")

    def test_version_is_0_16_1(self) -> None:
        assert azure_functions_doctor.__version__ == "0.16.1"  # pyright: ignore[reportUnknownMemberType]

    def test_version_is_string(self) -> None:
        assert isinstance(azure_functions_doctor.__version__, str)  # pyright: ignore[reportUnknownMemberType]
