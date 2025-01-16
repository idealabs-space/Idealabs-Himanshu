# utils/file_utils.py
import os

def save_readme(content: str, path: str) -> None:
    """
    Saves the README content to a file.
    """
    with open(os.path.join(path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(content)