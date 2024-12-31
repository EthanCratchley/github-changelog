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
    # Construct the file changes summary
    file_changes = "\n".join([
        f"File: {file.get('filename', 'Unknown')} | Status: {file.get('status', 'Unknown')} | "
        f"Patch: {file.get('patch', 'No patch available')[:500]}"
        for file in commit_info.get("files", [])
    ])

    if not file_changes:
        file_changes = "No files were changed in this commit."

    # Construct the prompt
    prompt = f"""
    A commit was made to a GitHub repository. Below are the details:

    **Commit Details:**
    - SHA: {commit_info.get('sha', 'Unknown')}
    - Author: {commit_info.get('author', 'Unknown')}
    - Date: {commit_info.get('date', 'Unknown')}
    - Message: {commit_info.get('message', 'No message provided')}

    **File Changes:**
    {file_changes}

    Please summarize this commit, describing its purpose and the key changes made.
    """

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled at summarizing code changes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5,
        )
        # Extract and return the summary
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        # Log or return the error
        return f"Error summarizing commit: {e}"
