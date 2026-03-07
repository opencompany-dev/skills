#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def normalize_action(skill: dict, action: dict) -> dict:
    normalized = dict(action)
    normalized.setdefault("integration", skill["integration"])
    normalized.setdefault("provider", skill["provider"])
    normalized.setdefault("description", "")
    return normalized


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    dist = repo / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    manifests = sorted(repo.glob("*/opencompany-skill.yaml"))
    skills = []
    for manifest_path in manifests:
        data = load_manifest(manifest_path)
        actions = [normalize_action(data, action) for action in data.get("actions", [])]
        skills.append(
            {
                "name": data["name"],
                "description": data["description"],
                "integration": data["integration"],
                "provider": data["provider"],
                "read_only": bool(data.get("read_only", False)),
                "actions": actions,
            }
        )

    bundle = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }

    output_path = dist / "skills-bundle.json"
    output_path.write_text(json.dumps(bundle, indent=2) + "\n")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
