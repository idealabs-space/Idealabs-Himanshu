# agents/repo_manager.py
import shutil
import tempfile
import os
import git
import stat
import errno

class RepoManager:
    def __init__(self):
        self.temp_dirs = []

    def clone_repository(self, repo_url: str) -> str:
        """
        Clones a GitHub repository to a temporary directory.
        """
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        
        try:
            git.Repo.clone_from(repo_url, temp_dir)
            return temp_dir
        except Exception as e:
            self.cleanup_directory(temp_dir)
            raise Exception(f"Failed to clone repository: {str(e)}")

    def cleanup_directory(self, directory_path: str) -> None:
        """
        Removes a temporary directory and its contents.
        Handles Windows permission errors gracefully.
        """
        if directory_path in self.temp_dirs:
            if os.path.exists(directory_path):
                try:
                    # On Windows, we need to handle read-only files
                    def handle_remove_readonly(func, path, exc):
                        excvalue = exc[1]
                        if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
                            # Ensure the file is writable
                            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                            # Retry the removal
                            func(path)
                        else:
                            raise excvalue

                    shutil.rmtree(directory_path, onerror=handle_remove_readonly)
                except Exception as e:
                    print(f"Warning: Failed to remove directory {directory_path}: {str(e)}")
            self.temp_dirs.remove(directory_path)

    def cleanup_all(self) -> None:
        """
        Cleans up all temporary directories created by this instance.
        """
        for dir_path in self.temp_dirs[:]:
            self.cleanup_directory(dir_path)