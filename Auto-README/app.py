import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Task
from langchain.tools import Tool
from agents.repo_manager import RepoManager
from agents.code_reviewer import CodeReviewer
from agents.readme_creator import ReadmeCreator
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import pyperclip

# Configuration
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=GEMINI_API_KEY)

# Configure the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7,
    google_api_key=GEMINI_API_KEY,
    convert_system_message_to_human=True
)

def create_task(agent, task_description, context=None):
    return Task(
        description=task_description,
        agent=agent,
        context=[context] if isinstance(context, dict) else context or [],
        expected_output="Detailed output based on the task",
        tools=[tool for tool in agent.tools]
    )

def generate_readme(repo_url):
    """Generate README content for a given repository URL"""
    with st.spinner("Initializing agents..."):
        # Initialize agents
        repo_manager = RepoManager()
        code_reviewer = CodeReviewer()
        readme_creator = ReadmeCreator(llm)

        # Create sequential tasks
        tasks = [
            create_task(
                repo_manager.agent,
                "Clone the GitHub repository and prepare for analysis",
                [{"description": "Clone repository", "repo_url": repo_url}]
            ),
            create_task(
                code_reviewer.agent,
                "Analyze repository contents and generate a comprehensive project summary",
                [{"description": "Analyze repository in detail"}]
            ),
            create_task(
                readme_creator.agent,
                "Generate a highly detailed and comprehensive README.md based on the analysis",
                [{"description": "Generate detailed README"}]
            )
        ]

        # Create and configure crew
        crew = Crew(
            agents=[repo_manager.agent, code_reviewer.agent, readme_creator.agent],
            tasks=tasks,
            verbose=True
        )

        try:
            with st.spinner("Processing repository..."):
                # Execute tasks sequentially
                repo_path = repo_manager.clone_repository(repo_url)
                if not repo_path:
                    st.error("Failed to clone repository")
                    return None

                project_summary = code_reviewer.analyze_repository(repo_path)
                if not project_summary:
                    st.error("Failed to analyze repository")
                    return None

                readme_content = readme_creator.create_readme(project_summary)
                if not readme_content:
                    st.error("Failed to generate README")
                    return None

                return readme_content

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Please check the repository URL and try again.")
            return None

def main():
    st.title("GitHub README Generator")
    st.write("Generate comprehensive README files for GitHub repositories")

    # Initialize session state for storing README content
    if 'readme_content' not in st.session_state:
        st.session_state.readme_content = None
    if 'repo_url' not in st.session_state:
        st.session_state.repo_url = ""

    # Repository URL input
    repo_url = st.text_input("Enter GitHub Repository URL", value=st.session_state.repo_url)
    
    # Create a row with two columns for the Generate and Refresh buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate README"):
            if not repo_url.strip():
                st.error("Please enter a valid GitHub Repository URL.")
            else:
                st.session_state.repo_url = repo_url
                st.session_state.readme_content = generate_readme(repo_url)

    with col2:
        if st.button("Refresh README"):
            if st.session_state.repo_url:
                st.session_state.readme_content = generate_readme(st.session_state.repo_url)
            else:
                st.warning("Please generate a README first before refreshing.")

    # Display README content if available
    if st.session_state.readme_content:
        st.success("README generated successfully!")

        # Create tabs for different views
        tab1, tab2 = st.tabs(["Raw Markdown", "Preview"])

        with tab1:
            # Store the README content in a text area
            readme_text = st.text_area(
                "README Content",
                value=st.session_state.readme_content,
                height=500,
                key="readme_raw"
            )

            # Copy button with confirmation
            if st.button("Copy to Clipboard"):
                try:
                    pyperclip.copy(st.session_state.readme_content)
                    st.success("Content copied to clipboard!")
                except Exception as e:
                    st.error(f"Failed to copy to clipboard: {str(e)}")

        with tab2:
            st.markdown(st.session_state.readme_content)

        # Download button
        st.download_button(
            label="Download README.md",
            data=st.session_state.readme_content,
            file_name="README.md",
            mime="text/markdown",
            key="download_btn",
            use_container_width=True
        )

if __name__ == "__main__":
    main()