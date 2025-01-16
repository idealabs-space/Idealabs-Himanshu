# main.py
import streamlit as st
import os
from dotenv import load_dotenv
from agents.repo_manager import RepoManager
from agents.code_analyzer import CodeAnalyzer
from agents.readme_generator import ReadmeGenerator
import time

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_readme(repo_url: str) -> str:
    """
    Generates README content for a given repository URL.
    """
    repo_manager = None
    try:
        with st.spinner("🔄 Initializing repository analysis..."):
            repo_manager = RepoManager()
            code_analyzer = CodeAnalyzer()
            readme_generator = ReadmeGenerator(GEMINI_API_KEY)

        with st.spinner("📥 Cloning repository..."):
            repo_path = repo_manager.clone_repository(repo_url)
            time.sleep(1)  # Give user time to see the progress

        with st.spinner("🔍 Analyzing repository structure..."):
            repo_analysis = code_analyzer.analyze_repository(repo_path)
            if not repo_analysis:
                raise ValueError("Repository analysis failed")
            time.sleep(1)  # Give user time to see the progress
            st.success("✅ Repository analysis completed")

        with st.spinner("📝 Generating README..."):
            readme_content = readme_generator.create_readme(repo_analysis)
            if not readme_content:
                raise ValueError("Failed to generate README content")

        return readme_content

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None
    finally:
        if repo_manager:
            repo_manager.cleanup_all()

def setup_page_style():
    """
    Sets up the custom CSS styling for the page.
    """
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .github-like {
            background-color: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 24px;
            margin: 10px 0;
        }
        .markdown-preview {
            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
            font-size: 16px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        .markdown-preview h1 {
            padding-bottom: 0.3em;
            border-bottom: 1px solid #eaecef;
            margin-bottom: 16px;
        }
        .markdown-preview h2 {
            padding-bottom: 0.3em;
            border-bottom: 1px solid #eaecef;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        .markdown-preview code {
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
        }
        .markdown-preview pre {
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="GitHub README Generator",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    setup_page_style()

    # Header Section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>📝 GitHub README Generator</h1>
            <p style='font-size: 1.2em; color: #586069;'>
                Generate professional README files for your GitHub repositories
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Main Content
    with st.container():
        # Repository URL input
        repo_url = st.text_input(
            "Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter the full URL of your GitHub repository"
        )

        # Generate README button
        if st.button("🚀 Generate README", type="primary", use_container_width=True):
            if not repo_url.strip():
                st.error("⚠️ Please enter a valid GitHub repository URL")
            elif not repo_url.startswith("https://github.com/"):
                st.error("⚠️ Please enter a valid GitHub repository URL starting with 'https://github.com/'")
            else:
                readme_content = generate_readme(repo_url)
                
                if readme_content:
                    st.success("✨ README generated successfully!")

                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📄 Raw Markdown", "👁️ Preview"])

                    with tab1:
                        col1, col2 = st.columns([5,1])
                        with col1:
                            readme_text = st.text_area(
                                "README Content",
                                value=readme_content,
                                height=600,
                                key="readme_raw"
                            )
                        with col2:
                            st.download_button(
                                "⬇️ Download",
                                data=readme_content,
                                file_name="README.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                            if st.button("📋 Copy", use_container_width=True):
                                try:
                                    st.write(readme_content, unsafe_allow_html=True)
                                    st.success("Copied!")
                                except Exception as e:
                                    st.error("Copy failed")

                    with tab2:
                        st.markdown("<div class='github-like markdown-preview'>", unsafe_allow_html=True)
                        st.markdown(readme_content)
                        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()