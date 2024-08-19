from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Upwork job search page
driver.get('https://www.upwork.com/nx/search/jobs/?client_hires=1-9,10-&nbs=1&payment_verified=1&q=annotation&sort=recency')

try:
    # Wait for the page to load and the job postings to be visible
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.card-list-container')))
    
    # Extract job postings
    job_posts = driver.find_elements(By.CSS_SELECTOR, 'section.card-list-container article.job-tile')
    
    with open('job_pool_database.txt', 'w', encoding='utf-8') as file:
        for job in job_posts:
            # Extract job title
            title_element = job.find_element(By.CSS_SELECTOR, 'h2.job-tile-title a')
            title = title_element.text
            job_url = title_element.get_attribute('href')
            
            # Extract job description (note: description may not be directly available in the search results)
            description_element = job.find_element(By.CSS_SELECTOR, 'p.mb-0.text-body-sm')
            description = description_element.text if description_element else "Description not available in search results"
            
            # Extract skills (if available)
            skills_container = job.find_element(By.CSS_SELECTOR, 'div.air3-token-container')
            skill_elements = skills_container.find_elements(By.CSS_SELECTOR, 'span.air3-token span')
            skills = [skill.text for skill in skill_elements]
            
            # Extract job posting date
            job_posted_date_element = job.find_element(By.CSS_SELECTOR, 'small[data-test="job-pubilshed-date"]')
            job_posted_date = job_posted_date_element.text if job_posted_date_element else "Date not available"

           
            # Write job details to file
            file.write(f"Title: {title}\n")
            file.write(f"URL: {job_url}\n")
            file.write(f"Description: {description}\n")
            file.write(f"Skills: {', '.join(skills)}\n")
            file.write(f"Job Posted Date: {job_posted_date}\n")
            file.write("-" * 40 + "\n")

finally:
    driver.quit()
