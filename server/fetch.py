from github import Github
import os

def fetch_commit_data(repo_name, num_commits):
    # Authenticate using access token
    access_token = os.getenv('ACCESS_TOKEN')
    if not access_token:
        raise ValueError("GitHub access token not found")

    g = Github(access_token)
    repo = g.get_repo(repo_name)

    # Initialize a list to organize commit data
    commit_data = []

    # Fetch commits
    commits = repo.get_commits()

    count = 0
    for commit in commits:
        if count >= num_commits:
            break

        # Handle cases where author or other fields may be None
        author_name = commit.commit.author.name if commit.commit.author else "Unknown"
        commit_date = commit.commit.author.date if commit.commit.author else "Unknown"

        commit_info = {
            "sha": commit.sha,
            "message": commit.commit.message,
            "author": author_name,
            "date": commit_date,
            "url": commit.html_url,
            "files": []
        }

        # Process file changes for each commit
        for file in (commit.files or []):  # Ensure files is iterable even if it's None
            file_info = {
                "filename": file.filename,
                "status": file.status,  # e.g., added, modified, removed
                "patch": getattr(file, 'patch', "No patch available")  # Safely access patch attribute
            }
            commit_info["files"].append(file_info)

        commit_data.append(commit_info)
        count += 1

    return commit_data
