#!/usr/bin/env python3
"""Validate distribution boundaries and build reproducible skills-only ZIPs."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ALLOWED_SUFFIXES = {".md", ".json", ".yaml", ".svg"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inside(package, value):
    require(value.startswith("./"), f"Package path needs ./ prefix: {value}")
    target = (package / value).resolve()
    require(target.is_relative_to(package.resolve()), f"Escaping package path: {value}")
    require(target.is_file(), f"Missing asset: {value}")
    return target


def validate(package):
    manifest = json.loads((package / "plugin.json").read_text())
    require(manifest["$schema"] == SCHEMA, "Unexpected package schema")
    require(manifest["name"] == package.name, "Package identity mismatch")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]), "Invalid name")
    require(len(manifest["name"]) <= 64, "Name too long")
    require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Invalid version")
    require(not (package / "mcp.json").exists(), "Unexpected MCP in skills-only package")
    extension = manifest["extensions"]["com.openai"]
    interface = extension["interface"]
    for field, limit in [("displayName", 30), ("shortDescription", 30),
                         ("longDescription", 4000), ("developerName", 80)]:
        require(isinstance(interface[field], str) and 0 < len(interface[field]) <= limit,
                f"Invalid {field}")
    require(interface["category"] == "Productivity", "Unexpected category")
    prompts = interface["defaultPrompt"]
    require(0 < len(prompts) <= 3 and len(set(prompts)) == len(prompts), "Invalid starter prompts")
    require(all(0 < len(p) <= 128 and "@" not in p for p in prompts), "Invalid prompt length")
    for field in ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"]:
        require(interface[field].startswith("https://") and len(interface[field]) <= 1024,
                f"Invalid {field}")
    inside(package, extension["onboardingSkill"])
    for field in ["logo", "composerIcon"]:
        icon = inside(package, interface[field])
        require(icon.stat().st_size <= 5 * 1024 * 1024, "Icon too large")
        svg = ElementTree.fromstring(icon.read_text())
        require(svg.attrib["width"] == svg.attrib["height"] and int(svg.attrib["width"]) >= 48,
                "Icon must be square and at least 48 pixels")
    files = sorted(p for p in package.rglob("*") if p.is_file())
    require(files and (package / "LICENSE").is_file(), "Missing license")
    skill_files = list((package / "skills").glob("*/SKILL.md"))
    require(skill_files, "No skills")
    for skill in skill_files:
        content = skill.read_text()
        require(content.startswith("---\n"), f"Missing frontmatter: {skill}")
        header = content.split("---", 2)[1]
        name = re.search(r"^name: (.+)$", header, re.M)
        description = re.search(r"^description: (.+)$", header, re.M)
        require(name and name.group(1) == skill.parent.name, f"Skill identity mismatch: {skill}")
        require(description and len(description.group(1)) <= 1024, f"Invalid description: {skill}")
        require(len(content.split("---", 2)[2].strip()) > 100, f"Empty instructions: {skill}")
    for path in files:
        require(not path.is_symlink(), f"Symlink in archive: {path}")
        require(path.name == "LICENSE" or path.suffix in ALLOWED_SUFFIXES, f"Unexpected file: {path}")
        require(not any(part.startswith(".") for part in path.relative_to(package).parts),
                f"Hidden file in archive: {path}")
        content = path.read_text()
        for pattern in [r"/Users/", r"/home/", r"-----BEGIN .*PRIVATE KEY-----", r"sk-[A-Za-z0-9_-]{20,}"]:
            require(not re.search(pattern, content), f"Private path or credential pattern: {path}")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            require(target.is_relative_to(package.resolve()) and target.is_file(),
                    f"Missing or external local reference: {path}: {link}")
    return manifest, files, len(skill_files)


def main():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    inventory = []
    for package in sorted((ROOT / "plugins").iterdir()):
        if not package.is_dir():
            continue
        manifest, files, skill_count = validate(package)
        archive = output / f"{manifest['name']}-{manifest['version']}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for path in files:
                info = zipfile.ZipInfo(path.relative_to(package).as_posix(), (2026, 10, 2, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, path.read_bytes())
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None, "Corrupt archive")
            require("plugin.json" in z.namelist(), "Manifest not at ZIP root")
            require(len(z.namelist()) == len(files), "ZIP inventory mismatch")
        record = {"name": manifest["name"], "version": manifest["version"], "skills": skill_count,
                  "files": len(files), "bytes": archive.stat().st_size,
                  "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
        inventory.append(record)
        print(f"PASS {record['name']}: {skill_count} skills, {len(files)} files, ZIP verified")
    (output / "inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
    print("Local structure checks passed. This does not establish OpenAI scan or listing approval.")


if __name__ == "__main__":
    main()
