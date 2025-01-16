# agents/readme_generator.py
import google.generativeai as genai
from typing import Dict

class ReadmeGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def create_readme(self, repo_analysis: Dict) -> str:
        """
        Creates a README.md file based on repository analysis.
        """
        prompt = self._generate_prompt(repo_analysis)
        
        try:
            response = self.model.generate_content(prompt)
            if not response or not response.text:
                raise ValueError("Failed to generate README content")
            return response.text
        except Exception as e:
            raise Exception(f"Error generating README: {str(e)}")

    def _generate_prompt(self, analysis: Dict) -> str:
        """
        Generates a focused prompt for README creation based on actual repository content.
        """
        languages = ', '.join(analysis['main_languages'])
        dependencies = ', '.join(analysis['dependencies'])
        
        # Create a structure overview
        structure = []
        for file in analysis['files']:
            structure.append(f"- {file.path}")
            if file.classes:
                structure.extend([f"  - Class: {cls}" for cls in file.classes])
            if file.functions:
                structure.extend([f"  - Function: {func}" for func in file.functions])

        prompt = f"""
        Create a clear and focused README.md for this repository. Focus only on existing features and actual implementation details.

        Repository Analysis:
        - Programming Languages: {languages}
        - Dependencies: {dependencies}

        Files and Structure:
        {chr(10).join(structure)}

        Please create a README.md with these guidelines:

        1. Title and Brief Description
           - Use the repository name as the title
           - Write a clear, factual description of what the project does
           - Do not include any badges or build status indicators

        2. Key Features
           - List only implemented features found in the codebase
           - Describe actual functionality, not planned features
           - Use specific examples from the code

        3. Prerequisites and Installation
           - List exact versions of required languages and tools: {languages}
           - Include actual dependencies found in the project: {dependencies}
           - Provide precise installation steps based on the project structure
           - Include any environment variables or configuration needed
           - Show real setup commands based on existing setup files

        4. Usage Instructions
           - Provide specific examples using actual code from the repository
           - Show real command-line usage if applicable
           - Include concrete examples of inputs and outputs
           - Document any configuration options that exist in the code
           - Show actual API endpoints or functions if they exist

        5. Project Structure
           - List only existing files and directories
           - Explain the purpose of each main component
           - Document key functions and classes that are implemented

        Formatting Requirements:
        - Use clear, standard Markdown
        - Include code blocks with appropriate language syntax highlighting
        - Keep sections focused and concise
        - Avoid placeholder content
        - Skip any sections (tests, contributing, etc.) that aren't actually implemented
        - Only mention supported features and platforms
        - Write in a clear, straightforward style

        Important Guidelines:
        1. Stay factual - only document what exists in the code
        2. Be specific - use real examples from the codebase
        3. Be concise - avoid unnecessary explanations
        4. Skip any sections not relevant to this specific project
        5. Focus on helping users understand and use the actual implementation

        The README should serve as an accurate guide to the current state of the project, not an idealized version.
        """
        return prompt