from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instantiate the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)


def summarize_commit(commit_info):
    """
    Summarizes a single commit using GPT-4o.

    Args:
        commit_info (dict): A dictionary containing the commit details:
            - sha: Commit SHA
            - message: Commit message
            - author: Commit author
            - date: Commit date
            - files: List of files with their changes

    Returns:
        str: Summary of the commit.
    """
    # Construct the prompt for GPT-4o
    file_changes = "\n".join([
        f"File: {file['filename']} | Status: {file['status']} | Patch: {file['patch'][:500]}"
        for file in commit_info.get("files", [])
    ])
    
    prompt = f"""
    A commit was made to a GitHub repository. Here are the details:

    Commit SHA: {commit_info['sha']}
    Author: {commit_info['author']}
    Date: {commit_info['date']}
    Message: {commit_info['message']}
    Changes:
    {file_changes}

    Please summarize this commit, describing its purpose and key changes.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Ensure you use the correct model ID
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled at summarizing code changes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error summarizing commit: {e}"

def main():
    # Example commit info
    example_commit = {
        "sha": "287f3a72825c17d0125bfae53c24b28b509a8892",
        "message": "file fixes and enhancements",
        "author": "Ethan Cratchley",
        "date": "2024-12-29T04:20:46Z",
        "files": [
            {"filename": ".gitignore", "status": "added", "patch": "@@ -0,0 +1,4 @@\n+.env\n+Procfile\n+LICENSE\n+CNAME\n\\ No newline at end of file"},
            {"filename": "README.md", "status": "modified", "patch": "@@ -76,3 +76,5 @@\n# Made By\n*- Ethan Cratchley*\n+\n+*As of Dec 2024 most likely not maintained*"}
        ]
    }

    # Summarize the commit
    summary = summarize_commit(example_commit)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main()
