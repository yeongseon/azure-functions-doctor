from collections import defaultdict
import importlib.resources
import json
from pathlib import Path
import time
from typing import Optional, TypedDict

from jsonschema import ValidationError, validate

from azure_functions_doctor.handlers import Rule, generic_handler
from azure_functions_doctor.logging_config import get_logger, log_rule_execution

logger = get_logger(__name__)


class CheckResult(TypedDict, total=False):
    label: str
    value: str
    status: str
    hint: str
    hint_url: str


class SectionResult(TypedDict):
    title: str
    category: str
    status: str  # 'pass' or 'fail'
    items: list[CheckResult]


class Doctor:
    """
    Diagnostic runner for Azure Functions apps.

    Loads checks from the built-in Azure Functions Python v2 rule asset
    located at `azure_functions_doctor.assets.rules.v2.json`.
    """

    def __init__(
        self,
        path: str = ".",
        profile: Optional[str] = None,
        rules_path: Optional[Path] = None,
    ) -> None:
        self.project_path: Path = Path(path).resolve()
        self.profile = profile
        self.rules_path: Optional[Path] = None
        if rules_path is not None:
            resolved = rules_path.resolve()
            if not resolved.is_file():
                raise ValueError(f"rules_path must be an existing file: {resolved}")
            self.rules_path = resolved
        self.programming_model = self._detect_programming_model()

    def _detect_programming_model(self) -> str:
        """Detect the Azure Functions programming model version.

        The doctor targets only the Azure Functions Python v2 programming
        model. Projects without decorators still default to "v2" so the
        doctor can report missing v2 signals as regular diagnostics.
        """
        if self._has_v2_decorators():
            return "v2"

        return "v2"

    def _has_v2_decorators(self) -> bool:
        """Check if the project uses v2 decorators using AST-based detection.

        Finds all FunctionApp() assignments to determine the app variable name,
        then checks for decorators of the form ``@<varname>.<method>`` via the AST.
        Falls back to checking the conventional ``app`` identifier when no
        assignment is found.
        """
        import ast as _ast

        python_files = list(self.project_path.rglob("*.py"))
        for py_file in python_files:
            try:
                source = py_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            try:
                tree = _ast.parse(source)
            except SyntaxError:
                continue

            # Collect all variable names assigned a FunctionApp() call.
            app_names: set[str] = set()
            for node in _ast.walk(tree):
                if isinstance(node, _ast.Assign):
                    if (
                        isinstance(node.value, _ast.Call)
                        and isinstance(node.value.func, _ast.Attribute)
                        and node.value.func.attr == "FunctionApp"
                    ):
                        for target in node.targets:
                            if isinstance(target, _ast.Name):
                                app_names.add(target.id)

            # If no FunctionApp assignment found, default to the conventional name.
            if not app_names:
                app_names = {"app"}

            def _decorator_uses_app(dec: _ast.expr, names: set[str] = app_names) -> bool:
                node: _ast.expr = dec.func if isinstance(dec, _ast.Call) else dec
                if isinstance(node, _ast.Attribute) and isinstance(node.value, _ast.Name):
                    return node.value.id in names
                return False

            for ast_node in _ast.walk(tree):
                if not isinstance(ast_node, (_ast.FunctionDef, _ast.ClassDef)):
                    continue
                for dec in ast_node.decorator_list:
                    if _decorator_uses_app(dec):
                        return True

        return False

    def load_rules(self) -> list[Rule]:
        """Load and validate rules from a custom path or the built-in v2 ruleset."""
        if self.rules_path is not None:
            with self.rules_path.open(encoding="utf-8") as f:
                rules: list[Rule] = json.load(f)
        else:
            rules = self._load_v2_rules()

        self._validate_rules(rules)
        return sorted(rules, key=lambda r: r.get("check_order", 999))

    def _validate_rules(self, rules: list[Rule]) -> None:
        schema_path = importlib.resources.files("azure_functions_doctor.schemas").joinpath(
            "rules.schema.json"
        )
        with schema_path.open(encoding="utf-8") as f:
            schema = json.load(f)

        try:
            validate(instance=rules, schema=schema)
        except ValidationError as exc:
            raise ValueError(f"Invalid rules file: {str(exc)}") from exc

    def _load_v2_rules(self) -> list[Rule]:
        """Load complete v2 rules set."""
        files_obj = importlib.resources.files("azure_functions_doctor.assets")

        # Load v2 rules from assets/rules/v2.json only
        try:
            rules_path = files_obj.joinpath("rules/v2.json")
            with rules_path.open(encoding="utf-8") as f:
                v2_rules = json.load(f)
        except FileNotFoundError as e:
            logger.error("v2.json not found")
            raise RuntimeError("v2.json not found") from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in v2.json: {e}")
            raise RuntimeError(f"Failed to parse v2.json: {e}") from e

        return sorted(list(v2_rules), key=lambda r: r.get("check_order", 999))

    def run_all_checks(self, rules: Optional[list[Rule]] = None) -> list[SectionResult]:
        rules = self.load_rules() if rules is None else rules
        if self.profile == "minimal":
            rules = [rule for rule in rules if rule.get("required", True)]
        elif self.profile not in (None, "full"):
            raise ValueError("Profile must be 'minimal' or 'full'")
        grouped: dict[str, list[Rule]] = defaultdict(list)

        for rule in rules:
            grouped[rule["section"]].append(rule)

        results: list[SectionResult] = []

        for section, checks in grouped.items():
            section_result: SectionResult = {
                "title": section.replace("_", " ").title(),
                "category": section,
                "status": "pass",
                "items": [],
            }

            for rule in checks:
                # Time rule execution for logging
                rule_start = time.time()
                result = generic_handler(rule, self.project_path)
                rule_duration_ms = (time.time() - rule_start) * 1000

                handler_status = result.get("status", "fail")
                log_rule_execution(rule["id"], rule["type"], handler_status, rule_duration_ms)

                # Simplified canonical mapping:
                # pass stays pass, otherwise required -> fail and optional -> warn.
                required = rule.get("required", True)
                if handler_status == "pass":
                    canonical = "pass"
                else:
                    canonical = "fail" if required else "warn"

                detail = result.get("detail", "")
                if canonical != "pass" and not required:
                    detail += " (optional)"

                item: CheckResult = {
                    "label": rule.get("label", rule["id"]),
                    "value": detail,
                    "status": canonical,
                }

                if canonical == "fail" and required:
                    section_result["status"] = "fail"

                if "hint" in rule:
                    item["hint"] = rule["hint"]

                if "hint_url" in rule and rule["hint_url"]:
                    item["hint_url"] = rule["hint_url"]

                section_result["items"].append(item)

            results.append(section_result)

        return results
