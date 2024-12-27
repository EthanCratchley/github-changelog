from github import Github
import os 

access_token = os.getenv('ACCESS_TOKEN')

g = Github(access_token)

#repo_name = input("What is your repo name?: ")
repo_name = 'EthanCratchley/winter-watch'
repo = g.get_repo(repo_name)

commits = repo.get_commits()

for commit in commits[:10]:  # Fetch the latest 10 commits
    print(f"Commit SHA: {commit.sha}")
    print(f"Message: {commit.commit.message}")
    print(f"Author: {commit.commit.author.name}")
    print(f"Date: {commit.commit.author.date}")
    print(f"URL: {commit.html_url}")
    print("-" * 40)

