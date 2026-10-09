
def main():
    print("================================")
    print("       NeuroCode AI")
    print("  GitHub Repository Analyzer")
    print("================================")

    repo_url = input("\nEnter GitHub repository URL: ").strip()

    if not repo_url:
        print("Error: Repository URL cannot be empty.")
        return

    if not repo_url.startswith("https://github.com/"):
        print("Error: Please enter a valid GitHub HTTPS URL.")
        return

    print(f"\nRepository URL received: {repo_url}")


if __name__ == "__main__":
    main()
