
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from fake_useragent import UserAgent

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

user_agent = "MyAwesomeScript v1.0 (https://upwork.com)"  # Replace with your details
os.environ["USER_AGENT"] = user_agent

user_agent = UserAgent().chrome 

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://www.upwork.com/agencies/1823322912407511040/")

documents = loader.load()

all_content = ""
for doc in documents:
    all_content += doc.page_content


current_dir = os.getcwd()

# Combine filename and path
filename = os.path.join(current_dir, "Datawox_upwork_profile_database.txt")

# Write the entire content to the text file
with open(filename, "w") as text_file:
    text_file.write(all_content)

