import os
import streamlit as st
import subprocess
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("GROQ_API_KEY")


st.set_page_config(layout='centered', page_title = "Datawox Job Matcher" )
st.title("Datawox Job Matcher")

client = Groq(
            api_key=KEY,
        )

def generate_review(profile, job_data):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are an expert Upwork profile and job details matcher explored for Datawox. Your objective is to analyze the provided Datawox Upwork profile and determine the best matches based on the provided job listings.
                    Ensure you return job listings that the data posted is less than a day.
                    Upwork profile: {profile}
                    Job listings: {job_data}

                    Provide the output of your analysis in this format and ensure there is a new line between job title, matching score and Job description:
                    Top 5 Job Listings:
                    1. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]

                    2. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]

                    3. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]

                    4. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]

                    5. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]
                    """,
                },
            ],
            model="llama-3.1-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating review: {e}")
        return None
    
def generate_coverLeter(job_pool_data, user_input, data_profile):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are an expert Upwork cover letter writter for Datawox team. Your objective is to
                    observe the job listings details carefully and craft a compelling and thrilling cover 
                    letter to apply for the top five job listings. Do this by leveraging on datawox upwork
                    profile {job_pool_data}. 
                    ensure the content of the cover letter is in human tone.
                    Ensure you use first person plural

                    review output: {data_profile}
                    User input: {user_input}
                    """,
                },
            ],
            model="llama-3.1-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating review: {e}")
        return None
    
col1, col2 = st.columns([1,1])
# Function to run the job bot script
def run_job_bot():
    subprocess.run(["python", "job_bot.py"])
    subprocess.run(["python", "database.py"])

# Button to start the job bot
with col1:
    if st.button("Start Job Bot"):
        with st.spinner('Scraping updated jobs...'):
            run_job_bot()
            st.success("Job bot completed!")   
        
        # Load the contents of the job_pool_database.txt and Datawox_upwork_profile_database.txt
        with st.spinner('Analysing Datawox and job similarites...'):
            try:
                with open("job_pool_database.txt", "r", encoding="utf-8") as job_file:
                    job_pool_data = job_file.read()
                with open("Datawox_upwork_profile_database.txt", "r", encoding="ISO-8859-1") as profile_file:
                    profile_data = profile_file.read()
                
                    review_output = generate_review(profile_data, job_pool_data)           
                  
            # Display the results
                if review_output:
                    st.markdown(review_output)

            except FileNotFoundError as e:
                st.error(f"Error: {e}. Please make sure the job bot has run successfully and the files exist.")
            st.success("Job bot task completed!")  

with col2:
    with open("job_pool_database.txt", "r", encoding="utf-8") as job_file:
                    job_pool_data = job_file.read()
    with open("Datawox_upwork_profile_database.txt", "r", encoding="ISO-8859-1") as profile_file:
        profile_data = profile_file.read()
    
        review_output = generate_review(profile_data, job_pool_data)
    user_input = st.text_input("Enter text here...")
    if user_input:
        with st.spinner('Generating cover letter...'):
            result = generate_coverLeter(review_output, user_input, profile_data)
                        # Display the results
            if result:
                st.markdown(result)
        st.success("Job bot task completed!")  
