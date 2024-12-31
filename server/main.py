from fetch import fetch_commit_data
from summarize import summarize_commit


def get_valid_repo():
    """Prompt the user to enter a valid GitHub username and repository."""
    while True:
        username = input("Enter the GitHub username (or type 'quit' to exit): ").strip()
        if username.lower() == "quit":
            return None, None

        repository = input("Enter the repository name: ").strip()
        if repository.lower() == "quit":
            return None, None

        repo_name = f"{username}/{repository}"
        try:
            # Test the repository validity by fetching 1 commit
            test_commits = fetch_commit_data(repo_name, 1)
            if test_commits:
                print(f"Successfully connected to repository: {repo_name}")
                return repo_name, test_commits
            else:
                print(f"No commits found in repository: {repo_name}. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please check the username and repository name and try again.")


def main():
    print("Welcome to the GitHub Commit Summarizer!")

    while True:
        # Get a valid repository
        repo_name, commits = get_valid_repo()
        if not repo_name:
            print("Goodbye!")
            break

        # Ask how many commits to fetch
        try:
            num_commits = int(input("How many commits would you like to fetch? "))
            if num_commits <= 0:
                raise ValueError("Number of commits must be greater than zero.")
        except ValueError:
            print("Invalid input. Fetching the latest 5 commits by default.")
            num_commits = 5

        print("\nFetching commits...")
        try:
            commits = fetch_commit_data(repo_name, num_commits)

            if not commits:
                print("No commits found in the repository.")
                continue

            # Display the commits in an organized list
            while True:
                print("\nFetched Commits:")
                for idx, commit in enumerate(commits, start=1):
                    print(f"{idx}. SHA: {commit['sha']} | Date: {commit['date']} | Message: {commit['message']}")

                # Allow user to select a commit for summarization
                try:
                    selection = int(
                        input("\nEnter the number of the commit you'd like summarized (or 0 to choose another repo): ")
                    )
                    if selection == 0:
                        break
                    if selection < 1 or selection > len(commits):
                        print(f"Please select a number between 1 and {len(commits)}.")
                        continue

                    selected_commit = commits[selection - 1]
                    print(f"\nSummarizing Commit {selected_commit['sha']}...")
                    summary = summarize_commit(selected_commit)
                    print("\nSummary:")
                    print(summary)

                    # Ask if the user wants to summarize another commit or switch repos
                    action = input("\nDo you want to (1) Summarize another commit, (2) Choose another repo, or (3) Quit? ")
                    if action == "1":
                        continue
                    elif action == "2":
                        break
                    elif action == "3":
                        print("Goodbye!")
                        return
                    else:
                        print("Invalid choice. Returning to the commit selection.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"Error fetching commits: {e}")


if __name__ == "__main__":
    main()
