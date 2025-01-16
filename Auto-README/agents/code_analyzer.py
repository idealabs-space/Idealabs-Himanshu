
# agents/code_analyzer.py
import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class FileAnalysis:
    path: str
    content: str
    size: int
    extension: str
    imports: List[str]
    classes: List[str]
    functions: List[str]

class CodeAnalyzer:
    def __init__(self):
        self.ignored_dirs = {'node_modules', 'venv', '.git', '__pycache__', 'build', 'dist'}
        self.supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.cs', '.go', '.rs'}
    
    def analyze_repository(self, repo_path: str) -> Dict:
        """
        Performs a comprehensive analysis of the repository structure and content.
        """
        analysis_result = {
            'files': [],
            'structure': {},
            'dependencies': set(),
            'main_languages': set(),
            'total_files': 0,
            'total_size': 0
        }

        for root, dirs, files in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                try:
                    if os.path.getsize(file_path) > 10 * 1024 * 1024:  # Skip files larger than 10MB
                        continue
                        
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext in self.supported_extensions:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            file_analysis = self._analyze_file(rel_path, content, file_ext)
                            analysis_result['files'].append(file_analysis)
                            analysis_result['total_files'] += 1
                            analysis_result['total_size'] += len(content)
                            analysis_result['main_languages'].add(file_ext[1:])  # Remove the dot
                            
                            # Extract dependencies
                            if file_ext == '.py':
                                analysis_result['dependencies'].update(self._extract_python_dependencies(content))
                            
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {str(e)}")
                    continue

        return analysis_result

    def _analyze_file(self, path: str, content: str, extension: str) -> FileAnalysis:
        """
        Analyzes individual file content and structure.
        """
        imports = []
        classes = []
        functions = []

        if extension == '.py':
            imports = self._extract_python_imports(content)
            classes = self._extract_python_classes(content)
            functions = self._extract_python_functions(content)

        return FileAnalysis(
            path=path,
            content=content[:1000],  # Store first 1000 chars for context
            size=len(content),
            extension=extension,
            imports=imports,
            classes=classes,
            functions=functions
        )

    def _extract_python_imports(self, content: str) -> List[str]:
        """Extract Python import statements."""
        imports = []
        for line in content.split('\n'):
            if line.strip().startswith(('import ', 'from ')):
                imports.append(line.strip())
        return imports

    def _extract_python_dependencies(self, content: str) -> set:
        """Extract Python package dependencies."""
        deps = set()
        for line in content.split('\n'):
            if line.strip().startswith(('import ', 'from ')):
                package = line.split()[1].split('.')[0]
                if package not in ['os', 'sys', 'typing', 'dataclasses']:
                    deps.add(package)
        return deps

    def _extract_python_classes(self, content: str) -> List[str]:
        """Extract Python class names."""
        classes = []
        for line in content.split('\n'):
            if line.strip().startswith('class '):
                class_name = line.split('class ')[1].split('(')[0].strip()
                classes.append(class_name)
        return classes

    def _extract_python_functions(self, content: str) -> List[str]:
        """Extract Python function names."""
        functions = []
        for line in content.split('\n'):
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                functions.append(func_name)
        return functions