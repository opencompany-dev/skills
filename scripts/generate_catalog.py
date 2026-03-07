#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def skill_dir(repo: Path, skill_name: str) -> Path:
    return repo / skill_name.split("/", 1)[1]


def action_summaries(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        return []
    manifest = load_json(manifest_path)
    integration = manifest.get("integration", "")
    provider = manifest.get("provider", "")
    out = []
    for action in manifest.get("actions", []):
        out.append(
            {
                "id": action["id"],
                "name": action["name"],
                "description": action.get("description", ""),
                "integration": action.get("integration", integration),
                "provider": action.get("provider", provider),
                "permission_action": action.get("permission_action", ""),
                "permission_resource": action.get("permission_resource", ""),
                "read_only": bool(action.get("read_only", False)),
            }
        )
    return out


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    dist = repo / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    index = load_json(repo / "index.yaml")
    skills = []
    for entry in index.get("skills", []):
        directory = skill_dir(repo, entry["name"])
        skill_md = directory / "SKILL.md"
        if not skill_md.exists():
            raise FileNotFoundError(f"missing {skill_md}")
        actions = action_summaries(directory / "opencompany-skill.yaml")
        skills.append(
            {
                "id": entry["name"],
                "name": entry["name"].split("/", 1)[1],
                "version": entry["version"],
                "description": entry["description"],
                "prompt_markdown": skill_md.read_text(),
                "actions": actions,
            }
        )

    bundle = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }
    output_path = dist / "skills-catalog.json"
    output_path.write_text(json.dumps(bundle, indent=2) + "\n")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
