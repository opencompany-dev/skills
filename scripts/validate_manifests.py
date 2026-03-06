#!/usr/bin/env python3
import json
import sys
from pathlib import Path


REQUIRED_SKILL_KEYS = {
    "version",
    "name",
    "description",
    "integration",
    "provider",
    "read_only",
    "actions",
}

REQUIRED_ACTION_KEYS = {
    "id",
    "name",
    "input_schema",
    "permission_action",
    "permission_resource",
    "read_only",
    "runner",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        fail(f"{path}: invalid JSON/YAML-JSON ({exc})")
    raise RuntimeError("unreachable")


def validate_input_schema(path: Path, action_id: str, schema: dict) -> None:
    if not isinstance(schema, dict):
        fail(f"{path}: action {action_id} input_schema must be an object")
    if schema.get("type") != "object":
        fail(f"{path}: action {action_id} input_schema.type must be 'object'")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        fail(f"{path}: action {action_id} input_schema.properties must be an object")
    additional = schema.get("additionalProperties")
    if additional is not False:
        fail(f"{path}: action {action_id} input_schema.additionalProperties must be false")
    required = schema.get("required", [])
    if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
        fail(f"{path}: action {action_id} input_schema.required must be an array of strings")
    missing_required = sorted(set(required) - set(properties.keys()))
    if missing_required:
        fail(
            f"{path}: action {action_id} input_schema.required references unknown properties: {', '.join(missing_required)}"
        )
    allowed_types = {"string", "integer", "boolean", "number"}
    for prop_name, prop_schema in properties.items():
        if not isinstance(prop_schema, dict):
            fail(f"{path}: action {action_id} property {prop_name} schema must be an object")
        prop_type = prop_schema.get("type")
        if prop_type not in allowed_types:
            fail(
                f"{path}: action {action_id} property {prop_name} type must be one of {', '.join(sorted(allowed_types))}"
            )


def validate_manifest(path: Path, manifest: dict, seen_action_ids: set[str]) -> None:
    missing = sorted(REQUIRED_SKILL_KEYS - set(manifest.keys()))
    if missing:
        fail(f"{path}: missing required keys: {', '.join(missing)}")
    if manifest["version"] != 2:
        fail(f"{path}: version must be 2")
    if manifest["read_only"] is not True:
        fail(f"{path}: read_only must be true")
    if not isinstance(manifest["actions"], list) or not manifest["actions"]:
        fail(f"{path}: actions must be a non-empty list")

    for action in manifest["actions"]:
        if not isinstance(action, dict):
            fail(f"{path}: action entry must be object")
        missing_action = sorted(REQUIRED_ACTION_KEYS - set(action.keys()))
        if missing_action:
            fail(
                f"{path}: action {action.get('id', '<missing id>')} missing keys: {', '.join(missing_action)}"
            )
        if action["read_only"] is not True:
            fail(f"{path}: action {action['id']} read_only must be true")
        validate_input_schema(path, action["id"], action["input_schema"])
        runner = action["runner"]
        if not isinstance(runner, dict) or "type" not in runner:
            fail(f"{path}: action {action['id']} missing runner.type")
        action_id = action["id"]
        if action_id in seen_action_ids:
            fail(f"{path}: duplicate action id '{action_id}'")
        seen_action_ids.add(action_id)


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    manifests = sorted(repo.glob("*/opencompany-skill.yaml"))
    if not manifests:
        fail("no manifests found")

    seen_action_ids: set[str] = set()
    for path in manifests:
        manifest = load_manifest(path)
        validate_manifest(path, manifest, seen_action_ids)

    print(f"Validated {len(manifests)} manifests and {len(seen_action_ids)} actions.")


if __name__ == "__main__":
    main()
