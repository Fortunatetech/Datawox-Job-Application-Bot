import os
from dotenv import load_dotenv
from fake_useragent import UserAgent

# Load environment variables from .env file
load_dotenv()

def scrape_upwork_profile(url: str, output_filename: str) -> str:
    # Set up user agent
    user_agent = "MyAwesomeScript v1.0 (https://upwork.com)"
    os.environ["USER_AGENT"] = user_agent
    user_agent = UserAgent().chrome

    # Load the content from the provided URL
    from langchain_community.document_loaders import WebBaseLoader
    loader = WebBaseLoader(url)
    documents = loader.load()

    # Combine the content of all pages into a single string
    all_content = ""
    for doc in documents:
        all_content += doc.page_content

    # Get the current working directory
    current_dir = os.getcwd()

    # Combine filename and path
    file_path = os.path.join(current_dir, output_filename)

    # Write the entire content to the text file
    with open(file_path, "w", encoding="utf-8") as text_file:
        text_file.write(all_content)

    # Return the scraped content
    return all_content