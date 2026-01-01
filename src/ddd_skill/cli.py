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
    # Step 1: Prompt for location if not specified
    if location is None:
        location = prompt_location()

    # Get available skills from the project
    available_skills = get_available_skills()

    if not available_skills:
        print("\n❌ 錯誤：專案中找不到任何 skills")
        print(f"預期位置：{SOURCE_SKILLS_DIR}")
        sys.exit(1)

    target_dir = get_skill_dir(location)
    location_label = "全域" if location == "global" else "當前專案"

    # Check if source and target are the same
    if SOURCE_SKILLS_DIR.resolve() == target_dir.resolve():
        print(f"\n✅ Skills 已經安裝在目標位置：{target_dir}")
        print("\n" + "=" * 70)
        print("已安裝的 Skills：")
        for skill_path in available_skills:
            skill_file = skill_path / "SKILL.md"
            description = ""
            if skill_file.exists():
                content = skill_file.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if line.startswith("description:"):
                        description = line.replace("description:", "").strip()
                        break
            print(f"  ✓ {skill_path.name}")
            if description:
                print(f"    {description}")
        print("=" * 70)
        print(f"\n共 {len(available_skills)} 個 skill(s) 可用！")
        return

    # Step 2: Start installation
    print(f"\n🚀 開始安裝 DDD Skills 到{location_label}...")
    print(f"目標位置：{target_dir}")

    # Check if directory needs to be created
    if not target_dir.exists():
        print(f"\n📁 建立目錄：{target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)
        print("   ✓ 目錄建立完成")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("安裝進度：")
    print()

    installed_skills = []

    # Step 3: Install each skill
    for idx, skill_path in enumerate(available_skills, 1):
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
        print(f"  [{idx}/{len(available_skills)}] ✓ {skill_name}")
        if description:
            print(f"      {description}")
        print()

    # Step 4: Show installation summary
    print("=" * 70)
    print(f"\n✅ 安裝完成！")
    print(f"\n已成功安裝 {len(installed_skills)} 個 skill(s) 到{location_label}")
    print(f"安裝位置：{target_dir}")
    print("\n已安裝的 Skills：")
    for skill_name, description in installed_skills:
        print(f"  • {skill_name}")
        if description:
            print(f"    {description}")
    print("\n" + "=" * 70)
    print("\n💡 使用方式：在 Claude Code 中輸入 /{skill_name} 即可使用")


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
