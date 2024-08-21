from job_bot import scrape_upwork_jobs

def main():
    # Call the scrape_upwork_jobs function from upwork_scraper module
    saved_file_path, job_details = scrape_upwork_jobs()
    
    # Use the returned values as needed
    print(f"Job details saved at: {saved_file_path}")
    for job in job_details:
        print(f"Job Title: {job['title']} - URL: {job['url']}")

if __name__ == "__main__":
    main()
