"""Tests for v2 programming model detection functionality."""

from pathlib import Path
import tempfile
from unittest.mock import patch

from azure_functions_doctor.doctor import Doctor


class TestProgrammingModelDetection:
    """Test v2-only programming model detection logic."""

    def test_detect_v2_with_decorators(self) -> None:
        """Test v2 detection when @app decorators are present."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            python_file = temp_path / "function_app.py"
            python_file.write_text("""
import azure.functions as func

app = func.FunctionApp()

@app.route(route="test", auth_level=func.AuthLevel.Anonymous)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello")
""")

            doctor = Doctor(str(temp_path))
            assert doctor.programming_model == "v2"

    def test_detect_v2_default_when_no_indicators(self) -> None:
        """Test v2 as the default when no decorators are found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            python_file = temp_path / "main.py"
            python_file.write_text("print('Hello World')")

            doctor = Doctor(str(temp_path))
            assert doctor.programming_model == "v2"

    def test_function_json_does_not_switch_to_v1(self) -> None:
        """Test that function.json files no longer change the supported model."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            function_json = temp_path / "function.json"
            function_json.write_text('{"scriptFile": "main.py", "entryPoint": "main"}')

            doctor = Doctor(str(temp_path))
            assert doctor.programming_model == "v2"

    def test_has_v2_decorators_with_various_patterns(self) -> None:
        """Test _has_v2_decorators with various @app patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_cases = [
                "@app.route(route='test')",
                "@app.schedule(schedule='0 */5 * * * *')",
                "@app.timer_trigger(schedule='0 */5 * * * *')",
                "@app.blob_trigger(arg_name='myblob', path='samples-workitems/{name}')",
                (
                    "@app.cosmos_db_trigger("
                    "arg_name='documents', database_name='ToDoList', "
                    "collection_name='Items')"
                ),
            ]

            for i, pattern in enumerate(test_cases):
                python_file = temp_path / f"test_{i}.py"
                python_file.write_text(f"""
import azure.functions as func

app = func.FunctionApp()

{pattern}
def test_function():
    pass
""")

                doctor = Doctor(str(temp_path))
                assert doctor.programming_model == "v2"

    def test_has_v2_decorators_ignores_comments(self) -> None:
        """Test that @app in comments does not count as a decorator."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            python_file = temp_path / "main.py"
            python_file.write_text("""
# This is a comment with @app.route but it should not count
print('Hello World')

def some_function():
    # Another comment with @app.schedule
    pass
""")

            doctor = Doctor(str(temp_path))
            assert doctor.programming_model == "v2"

    def test_has_v2_decorators_handles_file_read_errors(self) -> None:
        """Test that file read errors are handled gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            python_file = temp_path / "function_app.py"
            python_file.write_text("""
import azure.functions as func

app = func.FunctionApp()

@app.route(route="test", auth_level=func.AuthLevel.Anonymous)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello")
""")

            with patch("pathlib.Path.open", side_effect=OSError("Permission denied")):
                doctor = Doctor(str(temp_path))
                assert doctor.programming_model == "v2"

    def test_detect_v2_with_nested_decorators(self) -> None:
        """Test v2 detection with @app decorators in subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            nested_dir = temp_path / "functions"
            nested_dir.mkdir()

            python_file = nested_dir / "function_app.py"
            python_file.write_text("""
import azure.functions as func

app = func.FunctionApp()

@app.route(route="test", auth_level=func.AuthLevel.Anonymous)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello")
""")

            doctor = Doctor(str(temp_path))
            assert doctor.programming_model == "v2"
