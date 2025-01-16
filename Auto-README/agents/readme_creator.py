from crewai import Agent
from langchain.tools import Tool

class ReadmeCreator:
    def __init__(self, llm):
        self.llm = llm

        self.readme_tool = Tool(
            name="create_readme",
            func=self.create_readme,
            description="Creates README.md file from project summary"
        )

        self.agent = Agent(
            role='README Creator',
            goal='Create comprehensive README.md file which consists of a gist of everything that is present in the code and in a very creative and effective way',
            backstory='Expert technical writer specializing in documentation',
            tools=[self.readme_tool],
            llm=llm  # Changed from llm_model="local" to pass the LLM instance directly
        )

    def create_readme(self, project_summary):
        prompt = f"""
        Create a comprehensive README.md file for the following project:
        This is the summary of the project now create a README file which is professional below mentioned is one of the ways you can implement your own intelligence : {project_summary}
    
        
# Project Title

A clear and concise description of what the project does and its core purpose.

## Installation

```bash
git clone https://github.com/username/project.git
cd project
npm install  # or pip install -r requirements.txt
```

## Usage

```javascript
const projectModule = require('project');

// Basic example
const result = projectModule.mainFunction();
```

## Features

- Core feature 1: Detailed explanation of what it does and how it helps users
- Core feature 2: Key benefits and capabilities
- Core feature 3: Unique selling points and advantages

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

"""
        
        try:
            response = self.llm.predict(prompt)  # Changed from llm(prompt=prompt, max_tokens=1500)
            return response if response else "Failed to generate README"
        except Exception as e:
            return f"Error generating README: {str(e)}"