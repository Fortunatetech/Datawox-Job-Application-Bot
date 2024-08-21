import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Set up and return the WebDriver with headless Chrome."""
    logging.info("Setting up the WebDriver.")
   
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def extract_job_details(job):
    """Extract and return job details from a job element."""
    logging.info("Extracting job details.")
    title_element = job.find_element(By.CSS_SELECTOR, 'h2.job-tile-title a')
    title = title_element.text
    job_url = title_element.get_attribute('href')
    
# Extract job description
    try:
        description_element = job.find_element(By.CSS_SELECTOR, 'p.mb-0.text-body-sm')
        description = description_element.text
    except NoSuchElementException:
        description = "Description not available in search results"
    
    # Extract skills
    try:
        skills_container = job.find_element(By.CSS_SELECTOR, 'div.air3-token-container')
        skill_elements = skills_container.find_elements(By.CSS_SELECTOR, 'span.air3-token span')
        skills = [skill.text for skill in skill_elements]
    except NoSuchElementException:
        skills = []
    
    # Extract job posting date
    try:
        job_posted_date_element = job.find_element(By.CSS_SELECTOR, 'small[data-test="job-pubilshed-date"]')
        job_posted_date = job_posted_date_element.text
    except NoSuchElementException:
        job_posted_date = "Date not available"
    
    return {
        "title": title,
        "url": job_url,
        "description": description,
        "skills": ', '.join(skills),
        "job_posted_date": job_posted_date
    }

def save_job_details(jobs, filename='job_pool_database.txt'):
    """Save job details to a text file and return the file path and job details."""
    logging.info(f"Saving job details to {filename}.")
    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        for job in jobs:
            file.write(f"Title: {job['title']}\n")
            file.write(f"URL: {job['url']}\n")
            file.write(f"Description: {job['description']}\n")
            file.write(f"Skills: {job['skills']}\n")
            file.write(f"Job Posted Date: {job['job_posted_date']}\n")
            file.write("-" * 40 + "\n")
    
    logging.info("Job details saved successfully.")
    return filepath, jobs  # Returning both the file path and job details

def scrape_upwork_jobs():
    """Scrape Upwork jobs and return the file path of the saved job details and the details themselves."""
    driver = setup_driver()
    
    try:
        logging.info("Opening Upwork job search page.")
        driver.get('https://www.upwork.com/nx/search/jobs/?client_hires=1-9,10-&nbs=1&payment_verified=1&q=annotation&sort=recency')

        # Wait for the page to load and the job postings to be visible
        logging.info("Waiting for job postings to load.")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.card-list-container')))

        # Extract job postings
        job_posts = driver.find_elements(By.CSS_SELECTOR, 'section.card-list-container article.job-tile')
        logging.info(f"Found {len(job_posts)} job postings.")
        
        job_details = [extract_job_details(job) for job in job_posts]
        
        # Save job details and return the file path and details
        file_path, jobs = save_job_details(job_details)
        return file_path, jobs

    finally:
        logging.info("Quitting WebDriver.")
        driver.quit()