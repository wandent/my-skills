#!/usr/bin/env python3
"""
Initialize LESSONS_LEARNED.md for a project

Automatically creates LESSONS_LEARNED.md from template if it doesn't exist.
Can be run manually or called automatically before first lesson capture.

Usage:
    python init_lessons.py                    # Initialize in current directory
    python init_lessons.py /path/to/project   # Initialize in specific directory
    python init_lessons.py --force            # Force re-initialize (overwrite)
    python init_lessons.py --dry-run          # Show what would be created
"""

import sys
import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime


def get_template_path():
    """Get path to LESSONS_LEARNED.md.template"""
    # Template is in the same directory as this script
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / "LESSONS_LEARNED.md.template"
    return template_path


def init_lessons(project_path=".", force=False, dry_run=False):
    """
    Initialize LESSONS_LEARNED.md in the project directory.
    
    Args:
        project_path: Directory to initialize (default: current dir)
        force: Overwrite existing file (default: False)
        dry_run: Show what would be done without doing it (default: False)
    
    Returns:
        (success: bool, message: str)
    """
    project_path = Path(project_path)
    target_file = project_path / "LESSONS_LEARNED.md"
    template_path = get_template_path()

    # Validate template exists
    if not template_path.exists():
        return False, f"❌ Template not found: {template_path}"

    # Check if project directory exists
    if not project_path.exists():
        if dry_run:
            print(f"[DRY RUN] Would create directory: {project_path}")
            return True, f"[DRY RUN] Would create: {project_path}"
        
        try:
            project_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"❌ Failed to create directory: {str(e)}"

    # Check if file already exists
    if target_file.exists() and not force:
        return False, (
            f"⚠️  File already exists: {target_file}\n"
            f"   Use --force to overwrite or delete manually and re-run"
        )

    # Read template
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
    except Exception as e:
        return False, f"❌ Failed to read template: {str(e)}"

    # Update timestamp in template
    now = datetime.utcnow().isoformat() + "Z"
    updated_content = template_content.replace(
        'last_updated: "2026-04-22T14:30:00Z"',
        f'last_updated: "{now}"'
    )

    # Dry-run: show what would be written
    if dry_run:
        print(f"[DRY RUN] Would create: {target_file}")
        print(f"[DRY RUN] File size: {len(updated_content)} bytes")
        print(f"[DRY RUN] Timestamp: {now}")
        return True, "[DRY RUN] File initialization preview complete"

    # Write file
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(updated_content)
    except Exception as e:
        return False, f"❌ Failed to write file: {str(e)}"

    return True, f"✅ Created: {target_file}\n   Ready to capture your first lesson"


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Initialize LESSONS_LEARNED.md for a project"
    )
    parser.add_argument(
        "project",
        nargs="?",
        default=".",
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-initialize (overwrite existing file)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating it",
    )

    args = parser.parse_args()

    success, message = init_lessons(args.project, force=args.force, dry_run=args.dry_run)

    print(message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
