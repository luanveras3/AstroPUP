#!/usr/bin/env python3
"""
Update the repository tree section in README.md.

Usage:
    python tools/update_readme_tree.py

The README must contain these markers:

<!-- ASTROPUP_TREE_START -->
<!-- ASTROPUP_TREE_END -->
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

START = "<!-- ASTROPUP_TREE_START -->"
END = "<!-- ASTROPUP_TREE_END -->"

MAX_DEPTH = 3

EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
}

EXCLUDED_FILES = {
    ".DS_Store",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
}


def is_hidden(path: Path) -> bool:
    return path.name.startswith(".") and path.name != ".github"


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDED_DIRS or path.name in EXCLUDED_FILES:
        return True
    if path.suffix in EXCLUDED_SUFFIXES:
        return True
    if is_hidden(path):
        return True
    return False


def visible_children(path: Path):
    children = [p for p in path.iterdir() if not should_skip(p)]
    # Directories first, then files, both alphabetically.
    return sorted(children, key=lambda p: (p.is_file(), p.name.lower()))


def build_tree(path: Path, prefix: str = "", depth: int = 0):
    if depth >= MAX_DEPTH:
        return []

    children = visible_children(path)
    lines = []

    for index, child in enumerate(children):
        connector = "└── " if index == len(children) - 1 else "├── "
        display_name = child.name + "/" if child.is_dir() else child.name
        lines.append(prefix + connector + display_name)

        if child.is_dir():
            extension = "    " if index == len(children) - 1 else "│   "
            lines.extend(build_tree(child, prefix + extension, depth + 1))

    return lines


def generate_tree_block():
    lines = ["AstroPUP/"]
    lines.extend(build_tree(ROOT))
    return "```text\n" + "\n".join(lines) + "\n```"


def update_readme():
    if not README.exists():
        raise FileNotFoundError("README.md was not found.")

    text = README.read_text(encoding="utf-8")

    if START not in text or END not in text:
        raise ValueError(
            "README.md must contain the ASTROPUP_TREE_START and "
            "ASTROPUP_TREE_END markers."
        )

    before = text.split(START, 1)[0]
    rest = text.split(START, 1)[1]
    after = rest.split(END, 1)[1]

    new_section = START + "\n\n" + generate_tree_block() + "\n\n" + END
    new_text = before + new_section + after

    README.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print("README.md repository tree updated.")
