import json
from pathlib import Path
from typing import Any, TypedDict, cast


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class SchemaType(TypedDict):
    enum: list[str]


class SchemaCondition(TypedDict):
    properties: dict[str, Any]


class SchemaProperties(TypedDict):
    type: SchemaType
    condition: SchemaCondition


class SchemaItems(TypedDict):
    required: list[str]
    properties: SchemaProperties


class RuleSchema(TypedDict):
    items: SchemaItems


def _load_schema(path: Path) -> RuleSchema:
    schema = _load_json(path)
    assert isinstance(schema, dict)
    return cast(RuleSchema, schema)


def _load_rules(path: Path) -> list[dict[str, Any]]:
    rules = _load_json(path)
    assert isinstance(rules, list)
    return cast(list[dict[str, Any]], rules)


def test_rules_match_schema() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    schema_path = repo_root / "src/azure_functions_doctor/schemas/rules.schema.json"
    rules_path = repo_root / "src/azure_functions_doctor/assets/rules/v2.json"

    schema = _load_schema(schema_path)
    rules = _load_rules(rules_path)

    items = schema["items"]
    properties = items["properties"]
    condition_schema = properties["condition"]

    required_set = set(items["required"])
    allowed_types = set(properties["type"]["enum"])
    condition_props = set(condition_schema["properties"].keys())

    for rule in rules:
        missing = required_set - set(rule.keys())
        assert not missing, (
            f"Rule {rule.get('id', '<unknown>')} missing required fields: {sorted(missing)}"
        )

        rule_type = rule.get("type")
        assert rule_type in allowed_types, (
            f"Rule {rule.get('id', '<unknown>')} uses unknown type: {rule_type}"
        )

        condition = rule.get("condition")
        if isinstance(condition, dict):
            invalid_keys = set(condition.keys()) - condition_props
            assert not invalid_keys, (
                f"Rule {rule.get('id', '<unknown>')} has unsupported "
                f"condition fields: {sorted(invalid_keys)}"
            )
