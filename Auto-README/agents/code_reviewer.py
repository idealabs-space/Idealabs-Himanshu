# agents/code_reviewer.py
from crewai import Agent
from langchain.tools import Tool
import os

class CodeReviewer:
    def __init__(self):
        self.analyze_tool = Tool(
            name="analyze_repository",
            func=self.analyze_repository,
            description="Analyzes repository contents in detail and creates summary of what exactly was implemented in the repo"
        )

        self.agent = Agent(
            role='Code Reviewer',
            goal='Review each and every file in the repo and understand what was being implemented in the project and on the basis of it create a summary',
            backstory='You are an expert in analysing code and understands all the coding languages and terms in detail',
            tools=[self.analyze_tool],
            llm_model="local"
        )

    def analyze_repository(self, repo_path):
        summary = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if not file.startswith('.') and 'node_modules' not in root:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getsize(file_path) > 10 * 1024 * 1024:  # Skip files >10MB
                            continue
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            summary.append({
                                'file': os.path.relpath(file_path, repo_path),
                                'content': content[:1000]
                            })
                    except Exception as e:
                        print(f"Error reading file {file_path}: {str(e)}")
                        continue
        return self._generate_summary(summary)

    def _generate_summary(self, files_content):
        return "\n".join([f"- {f['file']}: {len(f['content'])} chars analyzed" for f in files_content])