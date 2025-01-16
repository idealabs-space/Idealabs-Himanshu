import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import openai
import time

# Agents

from agents.agent_resume_extractor import ResumeExtractionAgent
from agents.agent_job_search import JobSearchAgent
from agents.agent_csv_saver import CSVWriterAgent

# Load environment variables
load_dotenv()

# Configure OpenAI for Azure
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_ENDPOINT")
openai.api_version = os.getenv("API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt-4o")

def main():
    st.title("Job Finder App")

    st.markdown("""
    **Steps**:
    1. Upload your PDF resume.
    2. Enter the city where you want to find a job.
    3. We'll extract your skills (via GPT or another method) from your resume.
    4. Then we'll search multiple job sites (Indeed, LinkedIn, Glassdoor, Monster, etc.) **in multiple queries** 
       to find more listings (chunking your skill list).
    5. We match your skills with the job descriptions and return the **top 10** jobs in a CSV file.
    """)

    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    city = st.text_input("Enter your preferred city")

    if uploaded_file and city:
        if st.button("Find Jobs"):
            # Display a progress bar
            progress_bar = st.progress(0)
            current_progress = 0

            # 1. Extract skills from the resume
            with st.spinner("Extracting skills from your resume..."):
                resume_extractor = ResumeExtractionAgent(deployment_name=DEPLOYMENT_NAME)
                extracted_skills = resume_extractor.extract_skills(uploaded_file.read())
                time.sleep(1)  # Simulate some processing time

            current_progress += 30
            progress_bar.progress(current_progress)
            st.success("Skills extracted successfully!")
            st.write("**Extracted Skills**:", extracted_skills)

            # 2. Search for jobs (chunk-based) across multiple sites
            with st.spinner("Searching for relevant jobs... This may take a while if you have many skills..."):
                job_search_agent = JobSearchAgent()
                # You can adjust chunk_size if you like
                search_results = job_search_agent.search_jobs(
                    skills=extracted_skills,
                    city=city,
                    chunk_size=5
                )
                time.sleep(1)  # Simulate some processing time

            current_progress += 40
            progress_bar.progress(current_progress)

            # 3. Save the top 10 matched jobs to CSV
            with st.spinner("Matching skills & saving top jobs to CSV..."):
                csv_agent = CSVWriterAgent(filename="job_results.csv")
                csv_file_path = csv_agent.save_jobs_to_csv(
                    search_data=search_results,
                    user_skills=extracted_skills,
                    top_n=10  # Only top 10
                )
                time.sleep(1)  # Simulate some processing time

            current_progress += 30
            progress_bar.progress(current_progress)
            progress_bar.empty()

            st.success("Job search complete! See results below.")

            # 4. Display CSV
            if os.path.exists(csv_file_path):
                df = pd.read_csv(csv_file_path)
                st.dataframe(df)
            else:
                st.warning("No CSV file found or no results.")
        else:
            st.info("Click 'Find Jobs' to start searching.")
    else:
        st.info("Please upload a PDF resume and enter your city to begin.")

if __name__ == "__main__":
    main()
