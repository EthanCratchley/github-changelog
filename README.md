# GitHub Commit Summarizer
## Project Description
The GitHub Commit Summarizer is a tool that fetches commits from a GitHub repository and generates detailed, easy-to-understand summaries for them. Users can choose how they want the commits to be summarized—technical, brief, or non-technical—and even download the summaries as PDF files for further use.

This project is designed to streamline the process of understanding code changes, making it an invaluable tool for developers, team leads, and anyone working with GitHub repositories.

## Features
- Fetch Commits:
  - Retrieve a specified number of commits from any public (or authorized private) GitHub repository.

- Summarization Options:
  - Generate commit summaries in three different styles:
    1. Technical and Detailed
    2. Brief and Easy to Understand
    3. Brief and Non-Technical

- Export Summaries:
  - Download the generated summaries as well-formatted PDF files.

- Dynamic PDF Naming:
  - PDF files are automatically named using the first 5 characters of the commit SHA.

- Interactive Command-Line Interface:
  - Simple and user-friendly prompts guide users through every step.

## How to Run
### Prerequisites:
Before running the project, ensure you have the following installed on your machine:
- Python (version 3.8 or higher)
- Git
- GitHub Personal Access Token

### Steps:
1. Clone the Repository:
```bash
git clone https://github.com/EthanCratchley/github-changelog.git
cd github-changelog
```
2. Set Up a VM:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Dependencies:
```bash
pip install -r requirements.txt
```
4. Set Up Enviornment Variables:  
```bash
ACCESS_TOKEN=your_github_personal_access_token
OPENAI_API_KEY=your_openai_api_key
```
5. Run the Project

## Usage
1. Start the script using python main.py.
2. Follow the prompts:
   - Enter the GitHub username and repository name.
   - Specify how many commits you'd like to fetch.
   - Choose a commit to summarize.
   - Select a summarization style.
3. View the summary in the terminal.
4. Optionally, download the summary as a PDF.
5. Choose to summarize another commit, fetch a new repository, or quit the application.

## Technical Details
### Core Technologies
- Python:
  - Core language for logic and functionality.
- OpenAI API:
  - Summarization engine for generating human-readable commit summaries.
- ReportLab:
  - Library for generating PDFs.
- GitHub API:
  - Fetch commit data and repository details

## Contributing:
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: git checkout -b feature-name.
3. Commit your changes: git commit -m 'Add new feature'.
4. Push to your branch: git push origin feature-name.
5. Submit a pull request.

## Future Plans
- Integration with Slack, Discord, Teams:
  - Ability to interact and get information directly through other apps.
- Web Interface:
  - Build a web-based UI for an improved user experience.
- Bulk Summarization:
  - Allow users to summarize all fetched commits at once.
- Export Options:
  - Support additional export formats such as JSON, Markdown, and CSV.
- Repository Statistics:
  - Provide detailed insights about the repository, including contributor activity and most modified files.
- Code Suggestions:
  - Use AI to suggest code improvements based on commit diffs.
- Private Repository Support:
  - Streamline the use of personal access tokens for private repositories.

## Contact
For questions or suggestions, feel free to reach out:

Author: Ethan Cratchley <br>
Email: ethankcratchley@gmail.com <br>
Website: https://ethancratchley.com/ <br>
LinkedIn: https://www.linkedin.com/in/ethan-cratchley/ <br>
GitHub: https://github.com/EthanCratchley
