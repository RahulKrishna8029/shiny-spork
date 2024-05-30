import requests
import os
import json
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_as_pdf(pull_request, path):
    # Create a new PDF
    c = canvas.Canvas(path, pagesize=letter)

    # Set initial y position for writing text
    y_position = 700

    # Write pull request details to PDF
    for key, value in pull_request.items():
        text = f"{key.capitalize()}: {value}"
        c.drawString(100, y_position, text)
        y_position -= 20  # Adjust vertical position for the next line

    # Save the PDF
    c.save()

def pdf_to_markdown(pdf_path, markdown_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        # Write the text content to Markdown file
        with open(markdown_path, 'w') as md_file:
            md_file.write(text)

def get_closed_merged_pull_requests(repo_name, limit=10):
    base_url = "https://api.github.com/repos/{}/pulls".format(repo_name)
    params = {
        "state": "closed",
        "sort": "updated",
        "direction": "desc",
        "per_page": limit
    }
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return []

def main():
    repository_name = input("Enter the repository name:")
    limit = 10
    closed_merged_pull_requests = get_closed_merged_pull_requests(repository_name, limit)

    # Store the pull request objects
    stored_pull_requests = []

    for pr in closed_merged_pull_requests:
        if pr['merged_at']:
            stored_pull_requests.append(pr)

    # Example usage to print pull request titles
    for pr in stored_pull_requests:
        print(pr['title'])
    pdf_directory = "user directory paths"
    markdown_directory = "user directory paths"

    # Ensure the directories exist
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
    if not os.path.exists(markdown_directory):
        os.makedirs(markdown_directory)

    # Save the pull request data as a PDF and convert to Markdown
    for pr in stored_pull_requests:
        pull_request_data = pr
        pdf_path = os.path.join(pdf_directory, f"pull_request_{pull_request_data['number']}.pdf")
        markdown_path = os.path.join(markdown_directory, f"pull_request_{pull_request_data['number']}.md")
        save_as_pdf(pull_request_data, pdf_path)
        pdf_to_markdown(pdf_path, markdown_path)
        print(f"Pull request '{pull_request_data['title']}' saved as {pdf_path} and converted to Markdown as {markdown_path}")

if __name__ == "__main__":
    main()
