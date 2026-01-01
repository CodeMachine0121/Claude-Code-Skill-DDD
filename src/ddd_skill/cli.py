"""CLI for installing DDD skills to Claude Code."""

import argparse
import shutil
import sys
from pathlib import Path

# Get project root directory (where .claude/skills/ddd is located)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills" / "ddd"

GLOBAL_SKILL_DIR = Path.home() / ".claude" / "skills" / "ddd"
LOCAL_SKILL_DIR = Path.cwd() / ".claude" / "skills" / "ddd"


def get_available_skills() -> list[Path]:
    """Get list of available skill directories from the project."""
    if not SOURCE_SKILLS_DIR.exists():
        return []

    # Find all subdirectories that contain SKILL.md
    skills = []
    for item in SOURCE_SKILLS_DIR.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item)

    return sorted(skills)


def prompt_location() -> str:
    """Prompt user to choose installation location."""
    print("Where would you like to install the DDD skills?")
    print("")
    print("  [1] Global   (~/.claude/skills/ddd/)")
    print("      Available in all projects")
    print("")
    print("  [2] Local    (./.claude/skills/ddd/)")
    print("      Only available in this project")
    print("")

    while True:
        choice = input("Enter choice [1/2]: ").strip()
        if choice == "1":
            return "global"
        elif choice == "2":
            return "local"
        else:
            print("Invalid choice. Please enter 1 or 2.")


def get_skill_dir(location: str) -> Path:
    """Get the Claude Code skills directory based on location."""
    if location == "global":
        return GLOBAL_SKILL_DIR
    else:
        return LOCAL_SKILL_DIR


def install(location: str | None = None) -> None:
    """Install all DDD skills to Claude Code."""
    if location is None:
        location = prompt_location()

    # Get available skills from the project
    available_skills = get_available_skills()

    if not available_skills:
        print("Error: No skills found in the project.")
        print(f"Expected location: {SOURCE_SKILLS_DIR}")
        sys.exit(1)

    target_dir = get_skill_dir(location)

    # Check if source and target are the same
    if SOURCE_SKILLS_DIR.resolve() == target_dir.resolve():
        print(f"\nSkills are already installed at: {target_dir}")
        print("=" * 60)
        for skill_path in available_skills:
            print(f"  ✓ {skill_path.name} (already present)")
        print("=" * 60)
        print(f"\n{len(available_skills)} skill(s) already available!")
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nInstalling DDD skills to: {target_dir}")
    print("=" * 60)

    installed_skills = []

    for skill_path in available_skills:
        skill_name = skill_path.name
        target_skill_dir = target_dir / skill_name

        # Copy the skill directory
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)

        shutil.copytree(skill_path, target_skill_dir)

        # Read skill description from SKILL.md
        skill_file = target_skill_dir / "SKILL.md"
        description = ""
        if skill_file.exists():
            content = skill_file.read_text(encoding="utf-8")
            # Extract description from frontmatter
            for line in content.split("\n"):
                if line.startswith("description:"):
                    description = line.replace("description:", "").strip()
                    break

        installed_skills.append((skill_name, description))
        print(f"  ✓ {skill_name}")
        if description:
            print(f"    {description}")

    location_label = "globally" if location == "global" else "locally"
    print("=" * 60)
    print(f"\nSuccessfully installed {len(installed_skills)} skill(s) {location_label}!")
    print("\nInstalled skills:")
    for skill_name, description in installed_skills:
        print(f"  - {skill_name}")


def uninstall(location: str | None = None) -> None:
    """Uninstall all DDD skills from Claude Code."""
    if location is None:
        location = prompt_location()

    skill_dir = get_skill_dir(location)

    if skill_dir.exists():
        # Count skills before removal
        skill_count = sum(1 for item in skill_dir.iterdir() if item.is_dir())

        shutil.rmtree(skill_dir)
        location_label = "global" if location == "global" else "local"
        print(f"DDD skills ({location_label}) uninstalled from: {skill_dir}")
        print(f"Removed {skill_count} skill(s).")
    else:
        print("DDD skills are not installed at this location.")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="ddd-skill",
        description="Install or uninstall DDD skills for Claude Code",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install all DDD skills",
    )
    install_group = install_parser.add_mutually_exclusive_group()
    install_group.add_argument(
        "-g", "--global",
        action="store_true",
        dest="global_install",
        help="Install globally to ~/.claude/skills/ddd/",
    )
    install_group.add_argument(
        "-l", "--local",
        action="store_true",
        dest="local_install",
        help="Install locally to ./.claude/skills/ddd/",
    )

    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall",
        help="Uninstall all DDD skills",
    )
    uninstall_group = uninstall_parser.add_mutually_exclusive_group()
    uninstall_group.add_argument(
        "-g", "--global",
        action="store_true",
        dest="global_install",
        help="Uninstall from ~/.claude/skills/ddd/",
    )
    uninstall_group.add_argument(
        "-l", "--local",
        action="store_true",
        dest="local_install",
        help="Uninstall from ./.claude/skills/ddd/",
    )

    return parser


def main() -> None:
    """CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Determine location
    location: str | None = None
    if getattr(args, "global_install", False):
        location = "global"
    elif getattr(args, "local_install", False):
        location = "local"

    if args.command == "install":
        install(location)
    elif args.command == "uninstall":
        uninstall(location)


if __name__ == "__main__":
    main()
