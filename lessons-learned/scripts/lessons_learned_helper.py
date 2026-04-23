#!/usr/bin/env python3
"""
Lessons Learned Helper Module

Helper functions for agents and scripts to work with LESSONS_LEARNED.md files.
Can be imported directly into agent code or used as a library.

Example usage:
    from lessons_learned_helper import ensure_initialized, capture_standard
    
    # Ensure file exists before capturing
    ensure_initialized(".")
    
    # Add a new standard
    capture_standard(".", 
        category="process",
        title="Test Before Deploy",
        standard="Always test on staging first",
        context="Prevent production issues",
        action="Run test suite, verify staging, then deploy",
        priority="HIGH"
    )
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


class LessonsHelper:
    """Helper class for managing LESSONS_LEARNED.md files"""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.file_path = self.project_path / "LESSONS_LEARNED.md"

    def exists(self) -> bool:
        """Check if LESSONS_LEARNED.md exists"""
        return self.file_path.exists()

    def ensure_initialized(self) -> Tuple[bool, str]:
        """
        Ensure LESSONS_LEARNED.md exists.
        Auto-creates from template if missing.
        
        Returns:
            (success: bool, message: str)
        """
        if self.exists():
            return True, f"✅ File exists: {self.file_path}"

        # Import initialization function
        try:
            from init_lessons import init_lessons
            success, message = init_lessons(str(self.project_path), force=False, dry_run=False)
            return success, message
        except ImportError:
            return False, "❌ Could not import init_lessons module"

    def read(self) -> Optional[str]:
        """Read file contents"""
        if not self.exists():
            return None
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None

    def write(self, content: str) -> bool:
        """Write file contents"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False

    def parse_metadata(self) -> Dict:
        """Extract and parse YAML metadata"""
        content = self.read()
        if not content or not content.startswith("---"):
            return {}

        try:
            parts = content.split("---")
            if len(parts) >= 3:
                yaml_str = parts[1]
                metadata = {}
                for line in yaml_str.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip().strip("\"'")
                        
                        # Parse lists
                        if value.startswith("["):
                            value = [v.strip().strip("\"',") for v in value[1:-1].split(",")]
                        
                        metadata[key] = value
                return metadata
        except Exception as e:
            print(f"⚠️  Error parsing metadata: {e}")
            return {}

    def update_metadata(self, version: Optional[str] = None, update_timestamp: bool = True) -> bool:
        """Update version and/or timestamp in metadata"""
        content = self.read()
        if not content:
            return False

        if update_timestamp:
            now = datetime.utcnow().isoformat() + "Z"
            content = re.sub(
                r'last_updated:\s*"[^"]*"',
                f'last_updated: "{now}"',
                content
            )

        if version:
            content = re.sub(
                r'version:\s*"[^"]*"',
                f'version: "{version}"',
                content
            )

        return self.write(content)

    def get_version(self) -> Optional[str]:
        """Get current version"""
        metadata = self.parse_metadata()
        return metadata.get("version")

    def increment_version(self) -> Optional[str]:
        """Increment version (1.0 → 1.1 → 1.2, 1.9 → 2.0)"""
        current = self.get_version()
        if not current:
            return None

        try:
            major, minor = map(int, current.split("."))
            minor += 1
            if minor >= 10:
                major += 1
                minor = 0
            new_version = f"{major}.{minor}"
            self.update_metadata(version=new_version, update_timestamp=True)
            return new_version
        except Exception as e:
            print(f"❌ Error incrementing version: {e}")
            return None

    def add_standard(
        self,
        category: str,
        title: str,
        standard: str,
        context: str = "",
        action: str = "",
        priority: str = "MEDIUM",
        enforced: str = "Manual"
    ) -> Tuple[bool, str]:
        """
        Add a new standard to the file.
        
        Args:
            category: Category name (e.g., "prerequisites", "process")
            title: Standard title
            standard: What should be done
            context: Why it matters
            action: How to implement it
            priority: HIGH, MEDIUM, LOW
            enforced: Manual, Automated, Recommended
        
        Returns:
            (success: bool, message: str)
        """
        # Ensure file exists
        if not self.exists():
            success, msg = self.ensure_initialized()
            if not success:
                return False, f"❌ Failed to initialize: {msg}"

        content = self.read()
        if not content:
            return False, "❌ Could not read file"

        # Build standard entry
        standard_entry = f"""
### {title}
- **Standard**: {standard}
- **Context**: {context}
- **Action**: {action}
- **Priority**: {priority}
- **Enforced**: {enforced}
"""

        # Find category section or create it
        category_header = f"## {category.replace('-', ' ').title()}"
        
        if category_header in content:
            # Insert after category header
            lines = content.split("\n")
            insert_idx = None
            for i, line in enumerate(lines):
                if line.strip() == category_header:
                    insert_idx = i + 1
                    # Find next section (##) or end of file
                    for j in range(i + 1, len(lines)):
                        if lines[j].startswith("##") and j != i:
                            insert_idx = j - 1
                            break
                    break
            
            if insert_idx:
                lines.insert(insert_idx, standard_entry.strip())
                content = "\n".join(lines)
        else:
            # Add new category before "## Coding Standards" or at end
            if "## Coding Standards" in content:
                content = content.replace(
                    "## Coding Standards",
                    f"{category_header}\n{standard_entry.strip()}\n\n---\n\n## Coding Standards"
                )
            else:
                content = content.rstrip() + f"\n\n{category_header}\n{standard_entry.strip()}\n"

        # Update version and timestamp
        self.increment_version()

        # Write back
        if not self.write(content):
            return False, "❌ Failed to write file"

        return True, f"✅ Added to {category}: {title}"


# Module-level convenience functions

def ensure_initialized(project_path: str = ".") -> bool:
    """Ensure LESSONS_LEARNED.md exists (convenience function)"""
    helper = LessonsHelper(project_path)
    success, _ = helper.ensure_initialized()
    return success


def capture_standard(
    project_path: str = ".",
    category: str = "process",
    title: str = "",
    standard: str = "",
    context: str = "",
    action: str = "",
    priority: str = "MEDIUM",
    enforced: str = "Manual"
) -> bool:
    """Capture a new standard (convenience function)"""
    helper = LessonsHelper(project_path)
    success, message = helper.add_standard(
        category=category,
        title=title,
        standard=standard,
        context=context,
        action=action,
        priority=priority,
        enforced=enforced
    )
    if not success:
        print(message)
    return success


def get_high_priority_standards(project_path: str = ".") -> list:
    """Get all HIGH-priority standards (convenience function)"""
    # This would require full parsing; simplified version
    helper = LessonsHelper(project_path)
    content = helper.read()
    if not content:
        return []
    
    # Simple regex to find HIGH priority standards
    pattern = r"### (.+?)\n([\s\S]*?)\n- \*\*Priority\*\*: HIGH"
    matches = re.findall(pattern, content)
    return [match[0] for match in matches]


if __name__ == "__main__":
    # Self-test
    print("Lessons Learned Helper Module")
    print("Import this module to use LessonsHelper class or convenience functions")
    
    # Example:
    helper = LessonsHelper(".")
    if helper.exists():
        print(f"✅ Found: {helper.file_path}")
        print(f"Version: {helper.get_version()}")
    else:
        print(f"⚠️  Not found: {helper.file_path}")
        print("Run: python init_lessons.py")
