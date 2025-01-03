from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv
import textwrap

# Load environment variables
load_dotenv()

# Instantiate the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)


def summarize_commit(commit_info, summary_type):
    """
    Summarizes a commit based on the chosen summary type without using Markdown styling.
    """
    # Construct the file changes summary
    file_changes = "\n".join([
        f"File: {file.get('filename', 'Unknown')} | Status: {file.get('status', 'Unknown')} | "
        f"Patch: {file.get('patch', 'No patch available')[:500]}"
        for file in commit_info.get("files", [])
    ])

    if not file_changes:
        file_changes = "No files were changed in this commit."

    # Customize the prompt based on summary type
    summary_styles = {
        1: "Provide a detailed and technical summary of the commit. Avoid using any Markdown styling.",
        2: "Provide a brief and easy-to-understand summary of the commit. Avoid using any Markdown styling.",
        3: "Provide a brief, non-technical summary of the commit suitable for a general audience. Avoid using any Markdown styling."
    }
    summary_instruction = summary_styles.get(summary_type, summary_styles[2])

    # Construct the prompt
    prompt = f"""
    A commit was made to a GitHub repository. Below are the details:

    Commit Details:
    - SHA: {commit_info.get('sha', 'Unknown')}
    - Author: {commit_info.get('author', 'Unknown')}
    - Date: {commit_info.get('date', 'Unknown')}
    - Message: {commit_info.get('message', 'No message provided')}

    File Changes:
    {file_changes}

    {summary_instruction}
    """

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled at summarizing code changes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.5,
        )
        # Extract and return the summary
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error summarizing commit: {e}"

def save_summary_as_pdf(summary, file_name="commit_summary.pdf"):
    """
    Saves the summary as a plain text PDF with proper line wrapping and formatting.
    """
    try:
        # Initialize the PDF canvas
        c = canvas.Canvas(file_name, pagesize=letter)
        c.setFont("Helvetica", 10)
        width, height = letter
        margin = 50
        y = height - margin
        line_height = 12

        # Wrap text to fit the page width
        wrapper = textwrap.TextWrapper(width=90)  # Adjust width for line length
        wrapped_lines = []
        for line in summary.split("\n"):
            wrapped_lines.extend(wrapper.wrap(line))

        # Write each line to the PDF
        for line in wrapped_lines:
            if y <= margin:  # Start a new page if needed
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - margin
            c.drawString(margin, y, line)
            y -= line_height

        c.save()
        print(f"Summary saved as PDF: {file_name}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

