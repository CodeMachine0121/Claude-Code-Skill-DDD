"""CLI for installing DDD skills to Claude Code."""

import argparse
import shutil
import sys
from pathlib import Path

# For Python 3.9+, use importlib.resources
try:
    from importlib.resources import files
except ImportError:
    # Fallback for Python < 3.9
    from importlib_resources import files  # type: ignore

# Get skills directory from package resources
SOURCE_SKILLS_DIR = Path(str(files("ddd_skill").joinpath("skills")))

GLOBAL_SKILL_DIR = Path.home() / ".claude" / "skills"
LOCAL_SKILL_DIR = Path.cwd() / ".claude" / "skills"


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
    print("  [1] Global   (~/.claude/skills/)")
    print("      Available in all projects")
    print("")
    print("  [2] Local    (./.claude/skills/)")
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
    # Step 1: Prompt for location if not specified
    if location is None:
        location = prompt_location()

    # Get available skills from the project
    available_skills = get_available_skills()

    if not available_skills:
        print(f"\nError: No skills found at {SOURCE_SKILLS_DIR}")
        sys.exit(1)

    target_dir = get_skill_dir(location)

    # Check if source and target are the same
    if SOURCE_SKILLS_DIR.resolve() == target_dir.resolve():
        print(f"\nSkills already at: {target_dir}")
        for skill_path in available_skills:
            print(f"  ✓ {skill_path.name}")
        print(f"\n{len(available_skills)} skill(s) available")
        return

    # Start installation
    print(f"\nInstalling to {target_dir}\n")

    # Create directory if needed
    target_dir.mkdir(parents=True, exist_ok=True)

    # Install each skill
    for skill_path in available_skills:
        skill_name = skill_path.name
        target_skill_dir = target_dir / skill_name

        # Copy the skill directory
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)

        shutil.copytree(skill_path, target_skill_dir)
        print(f"  ✓ {skill_name}")

    # Show summary
    print(f"\nInstalled {len(available_skills)} skill(s). Use /{{skill_name}} to run.")


def uninstall(location: str | None = None) -> None:
    """Uninstall all DDD skills from Claude Code."""
    if location is None:
        location = prompt_location()

    skill_dir = get_skill_dir(location)

    # Get available skills from the package
    available_skills = get_available_skills()

    if not available_skills:
        print("\nError: No skills found in package")
        sys.exit(1)

    removed_count = 0

    print(f"\nUninstalling from {skill_dir}\n")

    # Remove each DDD skill
    for skill_path in available_skills:
        skill_name = skill_path.name
        target_skill_dir = skill_dir / skill_name

        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)
            print(f"  ✓ {skill_name}")
            removed_count += 1

    if removed_count > 0:
        print(f"\nRemoved {removed_count} skill(s)")
    else:
        print("\nNo DDD skills were installed")


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
        help="Install globally to ~/.claude/skills/",
    )
    install_group.add_argument(
        "-l", "--local",
        action="store_true",
        dest="local_install",
        help="Install locally to ./.claude/skills/",
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
        help="Uninstall from ~/.claude/skills/",
    )
    uninstall_group.add_argument(
        "-l", "--local",
        action="store_true",
        dest="local_install",
        help="Uninstall from ./.claude/skills/",
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
