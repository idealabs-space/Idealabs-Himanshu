import shutil
import tempfile
import os
from crewai import Agent
from langchain.tools import Tool
import git

class RepoManager:
    def __init__(self):
        self.clone_tool = Tool(
            name="clone_repository",
            func=self.clone_repository,
            description="Clones a GitHub repository to a temporary directory"
        )

        self.agent = Agent(
            role='Repository Manager',
            goal='Clone and manage GitHub repositories',
            backstory='Expert at handling Git repositories and file systems',
            tools=[self.clone_tool],
            llm_model="local"
        )

    def clone_repository(self, repo_url):
        temp_dir = tempfile.mkdtemp()
        try:
            repo = git.Repo.clone_from(repo_url, temp_dir)
            return temp_dir
        except Exception as e:
            # Cleanup on failure
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise Exception(f"Failed to clone repository: {str(e)}")

    def cleanup_directory(self, directory_path):
        """Ensures the directory is deleted properly."""
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
            except Exception as e:
                raise Exception(f"Failed to clean up temporary directory: {str(e)}")
