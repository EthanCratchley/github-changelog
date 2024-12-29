from github import Github
import os 

def fetch_commit_data(repo_name, num_commits):
    # Authenticate using access token
    access_token = os.getenv('ACCESS_TOKEN')
    if not access_token:
        raise ValueError("GitHub access token not found")

    # Repo Not Hard Coded 
    '''
    user_name = input("What is your username?: ")
    repository = input("What is your repository name?: ")
    repo_name = f'{user_name}/{repository}'
    '''

    g = Github(access_token)
    #repo_name = 'EthanCratchley/winter-watch'
    repo = g.get_repo(repo_name)

    # Initialize a dictionary to organize commit data
    commit_data = []

    # Fetch and process commits
    commits = repo.get_commits()

    for commit in commits[:num_commits]:  # Fetch the latest 3 commits
        commit_info = {
            "sha": commit.sha,
            "message": commit.commit.message,
            "author": commit.commit.author.name,
            "date": commit.commit.author.date,
            "url": commit.html_url,
            "files": []
        }
        
        # Process file changes for each commit
        for file in commit.files:
            file_info = {
                "filename": file.filename,
                "status": file.status,  # added, modified, removed
                "patch": file.patch  # Line-by-line changes
            }
            commit_info["files"].append(file_info)
        
        commit_data.append(commit_info)

        return commit_data

    '''
    # Print collected and organized data
    for commit in commit_data:
        print(f"Commit SHA: {commit['sha']}")
        print(f"Message: {commit['message']}")
        print(f"Author: {commit['author']}")
        print(f"Date: {commit['date']}")
        print(f"URL: {commit['url']}")
        print("Files:")
        for file in commit["files"]:
            print(f"  - File: {file['filename']}")
            print(f"    Status: {file['status']}")
            print(f"    Patch:\n{file['patch']}")
        print("-" * 40)
    '''
    
#fetch_commit_data('EthanCratchley/winter-watch')