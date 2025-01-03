from fetch import fetch_commit_data
from summarize import summarize_commit, save_summary_as_pdf


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
            # Test fetching commits to validate the repository
            test_commits = fetch_commit_data(repo_name, 1)
            if test_commits:
                print(f"Successfully connected to repository: {repo_name}")
                return repo_name, test_commits
            else:
                print(f"No commits found in repository: {repo_name}. Please try again.")
        except Exception as e:
            print(f"Error: {e}. Please check the username and repository name and try again.")


def main():
    """Main function to run the GitHub Commit Summarizer."""
    print("Welcome to the GitHub Commit Summarizer!")

    while True:
        # Get valid repository details
        repo_name, _ = get_valid_repo()
        if not repo_name:
            print("Goodbye!")
            break

        # Get the number of commits to fetch
        try:
            num_commits = int(input("How many commits would you like to fetch? "))
            if num_commits <= 0:
                raise ValueError("Number of commits must be greater than zero.")
        except ValueError:
            print("Invalid input. Fetching the latest 5 commits by default.")
            num_commits = 5

        print("\nFetching commits...")
        try:
            # Fetch the commits
            commits = fetch_commit_data(repo_name, num_commits)
            if not commits:
                print("No commits found in the repository.")
                continue

            while True:
                # Display the fetched commits
                print("\nFetched Commits:")
                for idx, commit in enumerate(commits, start=1):
                    print(f"{idx}. SHA: {commit['sha']} | Date: {commit['date']} | Message: {commit['message']}")

                # Select a commit for summarization
                try:
                    selection = int(input("\nEnter the number of the commit you'd like summarized (or 0 to choose another repo): "))
                    if selection == 0:
                        break
                    if selection < 1 or selection > len(commits):
                        print(f"Please select a number between 1 and {len(commits)}.")
                        continue

                    # Choose summarization type
                    print("\nHow would you like this to be summarized?")
                    print("1: Technical and Detailed")
                    print("2: Brief and Easy to Understand")
                    print("3: Quick and Non-Technical")

                    try:
                        summary_type = int(input("Choose an option (1, 2, or 3): "))
                        if summary_type not in [1, 2, 3]:
                            print("Invalid choice. Defaulting to Brief and Easy to Understand.")
                            summary_type = 2
                    except ValueError:
                        print("Invalid input. Defaulting to Brief and Easy to Understand.")
                        summary_type = 2

                    # Summarize the selected commit
                    selected_commit = commits[selection - 1]
                    print(f"\nSummarizing Commit {selected_commit['sha']}...")
                    summary = summarize_commit(selected_commit, summary_type)
                    print("\nSummary:")
                    print(summary)

                    # Option to download summary as PDF
                    download = input("\nDo you want to download the summary as a PDF? (yes/no): ").strip().lower()
                    if download == "yes":
                        pdf_filename = f"commit_{selected_commit['sha'][:5]}.pdf"
                        save_summary_as_pdf(summary, sha=selected_commit["sha"], file_name=pdf_filename)


                    # Next action options
                    action = input("\nDo you want to (1) Summarize another commit, (2) Choose another repo, or (3) Quit? ").strip()
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
