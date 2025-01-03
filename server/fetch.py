from github import Github
import os

def fetch_commit_data(repo_name, num_commits):
    """
    Fetch commit data from a given GitHub repository.

    Args:
        repo_name (str): The GitHub repository in the format "username/repo".
        num_commits (int): The number of commits to fetch.

    Returns:
        list: A list of dictionaries containing commit information.
    
    Raises:
        ValueError: If the GitHub access token is missing or invalid.
        Exception: For other errors during data fetching (e.g., invalid repo, API issues).
    """
    # Authenticate using access token
    access_token = os.getenv('ACCESS_TOKEN')
    if not access_token:
        raise ValueError("GitHub access token not found. Please set the ACCESS_TOKEN environment variable.")

    g = Github(access_token)
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        raise Exception(f"Unable to access repository '{repo_name}'. Please check the repository name and your access token. Error: {e}")

    # Initialize a list to organize commit data
    commit_data = []

    try:
        # Fetch commits from the repository
        commits = repo.get_commits()

        for count, commit in enumerate(commits):
            if count >= num_commits:
                break

            # Handle cases where author or other fields may be None
            author_name = commit.commit.author.name if commit.commit.author else "Unknown"
            commit_date = commit.commit.author.date if commit.commit.author else "Unknown"

            # Initialize commit information
            commit_info = {
                "sha": commit.sha,
                "message": commit.commit.message or "No message provided",
                "author": author_name,
                "date": commit_date,
                "files": []
            }

            # Process file changes for the commit
            for file in getattr(commit, 'files', []):  # Ensure 'files' attribute is handled safely
                file_info = {
                    "filename": getattr(file, 'filename', "Unknown"),
                    "status": getattr(file, 'status', "Unknown"),
                    "patch": getattr(file, 'patch', "No patch available")
                }
                commit_info["files"].append(file_info)

            commit_data.append(commit_info)
    except Exception as e:
        raise Exception(f"Error fetching commits from repository '{repo_name}': {e}")

    return commit_data
