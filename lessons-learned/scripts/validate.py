#!/usr/bin/env python3
"""
Lessons Learned Manager

Utilities for loading, validating, and managing LESSONS_LEARNED.md files.
Provides both CLI and library interfaces for agents and users.

Usage:
    python validate.py                    # Validate LESSONS_LEARNED.md in current dir
    python validate.py /path/to/file.md   # Validate specific file
    python validate.py --export json      # Export standards as JSON
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class Standard:
    """Represents a single standard entry"""
    category: str
    title: str
    standard: str
    context: str
    action: str
    priority: str  # HIGH, MEDIUM, LOW
    enforced: str  # Manual, Automated, Recommended

    def validate(self) -> List[str]:
        """Validate this standard for completeness"""
        errors = []
        if not self.standard:
            errors.append(f"{self.title}: Missing 'Standard' field")
        if not self.action:
            errors.append(f"{self.title}: Missing 'Action' field")
        if self.priority not in ["HIGH", "MEDIUM", "LOW"]:
            errors.append(f"{self.title}: Invalid priority '{self.priority}'")
        return errors


class LessonsLearned:
    """Parser and manager for LESSONS_LEARNED.md files"""

    def __init__(self, file_path: str = "LESSONS_LEARNED.md"):
        self.file_path = Path(file_path)
        self.metadata = {}
        self.standards: List[Standard] = []
        self.errors = []

    def load(self) -> bool:
        """Load and parse LESSONS_LEARNED.md"""
        if not self.file_path.exists():
            self.errors.append(f"File not found: {self.file_path}")
            return False

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse YAML front matter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    markdown_content = parts[2]

                    if yaml:
                        self.metadata = yaml.safe_load(yaml_content) or {}
                    else:
                        self.metadata = self._parse_yaml_simple(yaml_content)

                    self._parse_markdown(markdown_content)
                    return True

            self.errors.append("File does not contain YAML front matter (---)")
            return False

        except Exception as e:
            self.errors.append(f"Failed to load file: {str(e)}")
            return False

    def _parse_yaml_simple(self, yaml_str: str) -> Dict:
        """Simple YAML parser for basic key-value pairs"""
        result = {}
        for line in yaml_str.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"\'')

                # Parse lists
                if value.startswith("["):
                    value = [v.strip().strip("\"',") for v in value[1:-1].split(",")]

                result[key] = value
        return result

    def _parse_markdown(self, markdown_content: str):
        """Parse markdown sections to extract standards"""
        # Find all ### Section Title patterns
        section_pattern = r"###\s+(.+?)\n([\s\S]*?)(?=###\s|\Z)"
        
        current_category = None
        
        for match in re.finditer(section_pattern, markdown_content):
            title = match.group(1).strip()
            content = match.group(2).strip()

            # Detect category from ## headers
            if "##" in content:
                cat_match = re.search(r"##\s+(.+?)\n", content)
                if cat_match:
                    current_category = cat_match.group(1).strip()

            # Extract standard fields
            standard_match = re.search(r"\*\*Standard\*\*:\s*(.+?)(?:\n|$)", content)
            context_match = re.search(r"\*\*Context\*\*:\s*(.+?)(?:\n|$)", content)
            action_match = re.search(r"\*\*Action\*\*:\s*([\s\S]*?)(?=\n-\s\*\*|$)", content)
            priority_match = re.search(r"\*\*Priority\*\*:\s*(.+?)(?:\n|$)", content)
            enforced_match = re.search(r"\*\*Enforced\*\*:\s*(.+?)(?:\n|$)", content)

            if standard_match:
                standard = Standard(
                    category=current_category or "uncategorized",
                    title=title,
                    standard=standard_match.group(1).strip(),
                    context=context_match.group(1).strip() if context_match else "",
                    action=action_match.group(1).strip() if action_match else "",
                    priority=priority_match.group(1).strip() if priority_match else "MEDIUM",
                    enforced=enforced_match.group(1).strip() if enforced_match else "Manual",
                )

                validation_errors = standard.validate()
                self.errors.extend(validation_errors)
                self.standards.append(standard)

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the lessons learned file"""
        validation_errors = []

        # Check metadata
        required_meta = ["version", "last_updated", "categories"]
        for field in required_meta:
            if field not in self.metadata:
                validation_errors.append(f"Missing metadata field: {field}")

        # Check standards
        if not self.standards:
            validation_errors.append("No standards found in file")

        # Check for completeness
        for standard in self.standards:
            errors = standard.validate()
            validation_errors.extend(errors)

        all_errors = self.errors + validation_errors
        return len(all_errors) == 0, all_errors

    def get_high_priority(self) -> List[Standard]:
        """Get all HIGH-priority standards"""
        return [s for s in self.standards if s.priority == "HIGH"]

    def get_by_category(self, category: str) -> List[Standard]:
        """Get standards for a specific category"""
        return [s for s in self.standards if s.category == category]

    def get_by_priority(self, priority: str) -> List[Standard]:
        """Get standards by priority level"""
        return [s for s in self.standards if s.priority == priority]

    def export_json(self) -> str:
        """Export standards as JSON"""
        data = {
            "metadata": self.metadata,
            "standards": [asdict(s) for s in self.standards],
        }
        return json.dumps(data, indent=2)

    def export_report(self) -> str:
        """Generate a human-readable report"""
        lines = [
            "=" * 60,
            "LESSONS LEARNED REPORT",
            "=" * 60,
            "",
            f"Version: {self.metadata.get('version', 'unknown')}",
            f"Last Updated: {self.metadata.get('last_updated', 'unknown')}",
            "",
            "SUMMARY",
            "-" * 60,
        ]

        by_priority = {}
        for s in self.standards:
            p = s.priority
            if p not in by_priority:
                by_priority[p] = 0
            by_priority[p] += 1

        for priority in ["HIGH", "MEDIUM", "LOW"]:
            count = by_priority.get(priority, 0)
            lines.append(f"{priority}: {count} standards")

        lines.append("")
        lines.append("HIGH PRIORITY STANDARDS")
        lines.append("-" * 60)

        for s in self.get_high_priority():
            lines.append(f"\n[{s.category}] {s.title}")
            lines.append(f"  Standard: {s.standard}")
            lines.append(f"  Action: {s.action[:100]}...")

        if self.errors:
            lines.append("")
            lines.append("VALIDATION ERRORS")
            lines.append("-" * 60)
            for error in self.errors:
                lines.append(f"  ⚠️  {error}")

        return "\n".join(lines)


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Lessons Learned Manager")
    parser.add_argument(
        "file",
        nargs="?",
        default="LESSONS_LEARNED.md",
        help="Path to LESSONS_LEARNED.md file",
    )
    parser.add_argument(
        "--export",
        choices=["json", "report"],
        help="Export format",
    )
    parser.add_argument(
        "--high-priority",
        action="store_true",
        help="Show only HIGH-priority standards",
    )
    parser.add_argument(
        "--category",
        help="Show standards for specific category",
    )

    args = parser.parse_args()

    # Load file
    ll = LessonsLearned(args.file)
    if not ll.load():
        print(f"❌ Failed to load: {args.file}")
        for error in ll.errors:
            print(f"   {error}")
        sys.exit(1)

    # Validate
    is_valid, errors = ll.validate()
    if not is_valid:
        print("⚠️  Validation errors found:")
        for error in errors:
            print(f"   {error}")
        print()

    # Export or display
    if args.export == "json":
        print(ll.export_json())
    elif args.export == "report":
        print(ll.export_report())
    elif args.high_priority:
        standards = ll.get_high_priority()
        if not standards:
            print("No HIGH-priority standards found")
        else:
            print(f"🔴 {len(standards)} HIGH-priority standards:\n")
            for s in standards:
                print(f"  [{s.category}] {s.title}")
                print(f"    → {s.standard}\n")
    elif args.category:
        standards = ll.get_by_category(args.category)
        if not standards:
            print(f"No standards found for category: {args.category}")
        else:
            print(f"📋 Standards in '{args.category}':\n")
            for s in standards:
                print(f"  {s.title}")
                print(f"    Priority: {s.priority}")
                print(f"    Action: {s.action}\n")
    else:
        print(ll.export_report())

    if is_valid:
        print("\n✅ File is valid")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
