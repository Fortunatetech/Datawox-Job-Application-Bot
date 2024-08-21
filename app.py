import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from database import scrape_upwork_profile
from job_bot import scrape_upwork_jobs

load_dotenv()
KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(layout='centered', page_title = "Datawox Job Matcher" )
st.title("Datawox Job Matcher")

# Initialize session state for storing data
if 'datawox_profile_database' not in st.session_state:
    st.session_state.datawox_profile_database = None

if 'job_details' not in st.session_state:
    st.session_state.job_details = None

# Sidebar for refreshing data
with st.sidebar:
    st.title("Click the Refresh Data to Refresh Job Listings ")
    if st.button("Refresh Data"):
        with st.spinner("Refreshing data"):
            url = "https://www.upwork.com/agencies/1823322912407511040/"
            output_filename = "Datawox_upwork_profile_database.txt"
            st.session_state.datawox_profile_database = scrape_upwork_profile(url, output_filename)
            _, st.session_state.job_details = scrape_upwork_jobs()
            st.success("Data refreshed successfully!")

client = Groq( api_key=KEY )

def generate_review(datawox_profile_database, job_details):
    if datawox_profile_database is None or job_details is None:
        st.error("Please refresh the data first.")
        return None
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are an expert Upwork profile and job details matcher for Datawox. 
                    Your objective is to carefully study and understand the provided Datawox Upwork profile 
                    and determine the best matching job postings in the provided job postings.
                    Ensure you return job postings that the date posted is less than a day.
                    Datawox Upwork profile: {datawox_profile_database}
                    Job listings: {job_details}

                    Provide the output of your analysis in this format and ensure there is a new line between job title, matching score and Job description:
                    Top 3 Job Listings:
                    1. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]

                    2. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]

                    3. Job Title: [Title]
                       Matching Score: [Score]
                       Job Description: [Description]
                    """,
                },
            ],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating review: {e}")
        return None
    
def generate_cover_letter(job_details, datawox_profile_database, user_query):
    if datawox_profile_database is None or job_details is None:
        st.error("Please refresh the data first.")
        return None
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are an expert Upwork cover letter writter for Datawox team. Your objective is to
                    observe the job postings details, and Datawox profile carefully.
                    follow user query: {user_query}  and Craft a compelling 
                    and thrilling cover letter to secure the job. If job posting is similar to the Datawox
                    portfolio or work experience include it in the cover letter to make the application strong 
                    and convincing. 
                    Ensure the content of the cover letter is in human tone.
                    Ensure you use first person plural.
                    
                    Datawox Upwork profile: {datawox_profile_database}
                    Job listings: {job_details}
                    """,
                },
            ],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating review: {e}")
        return None
 
col1, col2 = st.columns([1,1])

with col1:
    if st.button("Generate Updated Job Listings"):
        if st.session_state.datawox_profile_database is None or st.session_state.job_details is None:
            st.error("Please refresh the data first.")
        else:
            with st.spinner('Generating results...'):
                review_output = generate_review(st.session_state.datawox_profile_database, st.session_state.job_details)
                st.success("Job bot completed!")
                if review_output:
                    st.markdown(review_output)

with col2:
    user_query = st.text_input("Ask me to generate a compelling and thrilling cover letter...")
    if user_query:
        if st.session_state.datawox_profile_database is None or st.session_state.job_details is None:
            st.error("Please refresh the data first.")
        else:
            with st.spinner('Generating cover letter...'):
                result = generate_cover_letter(st.session_state.job_details, st.session_state.datawox_profile_database, user_query)
                # Display the results
                if result:
                    st.markdown(result)
            st.success("Job bot task completed!")