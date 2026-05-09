# Automatic README repository tree updater

This package adds a small script that updates the repository structure section in `README.md`.

## Files included

```text
tools/update_readme_tree.py
.github/workflows/check-readme-tree.yml
```

## 1. Add the markers to README.md

Replace the current repository structure block in your README with this:

```md
## Repository structure

<!-- ASTROPUP_TREE_START -->

```text
AstroPUP/
```

<!-- ASTROPUP_TREE_END -->
```

## 2. Copy the files

Copy these into your repository:

```text
tools/update_readme_tree.py
.github/workflows/check-readme-tree.yml
```

## 3. Run locally

From the repository root:

```bash
python tools/update_readme_tree.py
```

This updates the README automatically.

## 4. Commit

```bash
git add README.md tools/update_readme_tree.py .github/workflows/check-readme-tree.yml
git commit -m "Add automatic README tree updater"
git push
```

## What the GitHub Action does

The workflow regenerates the tree and checks if `README.md` changed.

If the README tree is outdated, the action becomes red.

That is intentional: it tells you to run:

```bash
python tools/update_readme_tree.py
```

then commit the updated README.
