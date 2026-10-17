
from pathlib import Path
from git import Repo, GitCommandError

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "repos"


def clone_repository(repo_url: str):
    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    if not repo_name or repo_name in {".", ".."}:
        print("Error: Invalid repository name.")
        return None

    destination = REPOS_DIR / repo_name

    if destination.exists():
        print(f"Repository already exists: {destination}")
        return destination

    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nCloning repository: {repo_name}")
    print("Please wait...")

    try:
        Repo.clone_from(repo_url, str(destination))
        print("\nRepository cloned successfully!")
        print(f"Location: {destination}")
        return destination

    except GitCommandError as error:
        print(f"\nGit error: {error}")
        return None


def scan_python_files(repo_path: Path):
    ignored_dirs = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
    }

    python_files = []

    for file_path in repo_path.rglob("*.py"):
        relative_path = file_path.relative_to(repo_path)

        if any(part in ignored_dirs for part in relative_path.parts):
            continue

        python_files.append(relative_path)

    python_files.sort()

    print(f"\nPython files found: {len(python_files)}")
    print("\nFirst 20 Python files:")

    for file_path in python_files[:20]:
        print(f"  {file_path}")

    if len(python_files) > 20:
        print(f"  ...and {len(python_files) - 20} more.")

    return python_files


def main():
    print("================================")
    print("       NeuroCode AI")
    print("  GitHub Repository Analyzer")
    print("================================")

    repo_url = input("\nEnter GitHub repository URL: ").strip()

    if not repo_url.startswith("https://github.com/"):
        print("Error: Please enter a GitHub HTTPS URL.")
        return

    repo_path = clone_repository(repo_url)

    if repo_path is None:
        return

    scan_python_files(repo_path)


if __name__ == "__main__":
    main()
