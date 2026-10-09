
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
        return

    destination = REPOS_DIR / repo_name

    if destination.exists():
        print(f"Repository already exists: {destination}")
        return

    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nCloning repository: {repo_name}")
    print("Please wait...")

    try:
        Repo.clone_from(repo_url, str(destination))
        print("\nRepository cloned successfully!")
        print(f"Location: {destination}")

    except GitCommandError as error:
        print(f"\nGit error: {error}")


def main():
    print("================================")
    print("       NeuroCode AI")
    print("  GitHub Repository Analyzer")
    print("================================")

    repo_url = input("\nEnter GitHub repository URL: ").strip()

    if not repo_url.startswith("https://github.com/"):
        print("Error: Please enter a GitHub HTTPS URL.")
        return

    clone_repository(repo_url)


if __name__ == "__main__":
    main()
