# utils/file_utils.py
import os

def save_readme(content, path):
    with open(os.path.join(path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(content)