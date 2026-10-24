#!/usr/bin/env python3
"""
validate_skill.py - Anthropic Agent Skills / Claude Code Conformance Linter

Validates that a skill directory and its SKILL.md file strictly conform to:
1. Anthropic Agent Skills specification (agentskills.io)
2. Claude Code skill activation standards
"""

import sys
import os
import re
from pathlib import Path

def validate_skill_directory(skill_dir: Path) -> list[str]:
    errors = []
    
    if not skill_dir.is_dir():
        return [f"'{skill_dir}' is not a directory."]
        
    dir_name = skill_dir.name
    if dir_name.startswith("_") or dir_name.startswith("."):
        # Template or hidden directory
        pass
    else:
        # Check directory name format: lowercase alphanumeric and hyphens only, no consecutive hyphens
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", dir_name):
            errors.append(f"Directory name '{dir_name}' must be lowercase alphanumeric with single hyphens, matching regex ^[a-z0-9]+(-[a-z0-9]+)*$")
        if len(dir_name) > 64:
            errors.append(f"Directory name '{dir_name}' exceeds 64 characters ({len(dir_name)} chars).")

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return errors + [f"Missing required file: {skill_file}"]
        
    content = skill_file.read_text(encoding="utf-8")
    
    # 1. Check YAML frontmatter presence
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not frontmatter_match:
        errors.append("SKILL.md must begin with a YAML frontmatter block enclosed by '---'.")
        return errors
        
    frontmatter_raw = frontmatter_match.group(1)
    body = frontmatter_match.group(2)
    
    # Parse basic frontmatter key-values
    fields = {}
    current_key = None
    for line in frontmatter_raw.splitlines():
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
        key_match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if key_match:
            current_key = key_match.group(1)
            fields[current_key] = key_match.group(2).strip()
        elif current_key and line.startswith("  "):
            # Multi-line or continuation
            fields[current_key] += " " + line_stripped

    # 2. Validate 'name'
    if "name" not in fields or not fields["name"]:
        errors.append("Frontmatter is missing required field: 'name'.")
    else:
        name_val = fields["name"].strip("\"'")
        if len(name_val) > 64:
            errors.append(f"Field 'name' exceeds 64 characters ({len(name_val)}).")
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name_val):
            errors.append(f"Field 'name' ('{name_val}') must contain only lowercase letters, digits, and single hyphens.")
        if not dir_name.startswith("_") and name_val != dir_name:
            errors.append(f"Field 'name' ('{name_val}') does not match directory name ('{dir_name}').")

    # 3. Validate 'description'
    if "description" not in fields or not fields["description"]:
        errors.append("Frontmatter is missing required field: 'description'.")
    else:
        desc_val = fields["description"].strip("\"'")
        if len(desc_val) > 1024:
            errors.append(f"Field 'description' exceeds 1024 characters ({len(desc_val)}).")
        if "use when" not in desc_val.lower():
            errors.append("Field 'description' should contain explicit trigger criteria (e.g. 'Use when...').")

    # 4. Validate Markdown Body
    if not re.search(r"^#\s+.+", body, re.MULTILINE):
        errors.append("Body must contain a top-level Markdown title (# Title).")
        
    if not re.search(r"##\s+.*when to use", body, re.IGNORECASE):
        errors.append("Body should contain a 'When to Use' section explaining triggering scenarios.")
        
    if not re.search(r"-\s+\[\s*\]", body):
        errors.append("Body should contain a self-verification checklist (- [ ] task).")

    return errors

def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    
    if target.is_file() and target.name == "SKILL.md":
        targets = [target.parent]
    elif (target / "SKILL.md").exists():
        targets = [target]
    else:
        # Search all subdirectories containing SKILL.md
        targets = sorted([p.parent for p in target.glob("**/SKILL.md")])
        
    if not targets:
        print(f"No SKILL.md files found in {target}")
        sys.exit(1)
        
    total_errors = 0
    print(f"Validating {len(targets)} skill(s) against Claude Code & Anthropic Agent Skills standards...\n")
    
    for skill_dir in targets:
        errors = validate_skill_directory(skill_dir)
        skill_name = skill_dir.name
        if errors:
            print(f"❌ {skill_name}: FAILED")
            for e in errors:
                print(f"   • {e}")
            total_errors += len(errors)
        else:
            print(f"✅ {skill_name}: CONFORMANT")
            
    print(f"\nCompleted with {total_errors} issue(s).")
    sys.exit(0 if total_errors == 0 else 1)

if __name__ == "__main__":
    main()
