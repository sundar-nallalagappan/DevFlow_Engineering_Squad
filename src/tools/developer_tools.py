import os
import shutil
import subprocess
import sys
import stat

# --- CONFIGURATION ---
GITHUB_USERNAME = "sundar-nallalagappan"
GITHUB_TOKEN    = os.getenv('GITHUB_PAT')
REPO_NAME       = "Sales-Dashboard"         # The repo you created earlier
BRANCH_NAME     = "main"                    # or 'master', check your repo

# The URL includes the token so the Agent can push without typing a password
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# The folder where the Agent will download the code
WORKSPACE_DIR = "./agent_workspace"

print("✅ Configuration loaded.")

def on_rm_error(func, path, exc_info):
    """
    Error handler for shutil.rmtree.
    If the error is due to an access error (read-only file), 
    it attempts to add write permission and then deletes it.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)
    
def clone_repository():
    """
    Tools for the Agent to download the code from GitHub.
    It cleans up any old files first to ensure a fresh start.
    """
    try:
        # 1. Clean previous workspace if it exists
        if os.path.exists(WORKSPACE_DIR):
            shutil.rmtree(WORKSPACE_DIR, onerror=on_rm_error)
        
        # 2. Create directory
        os.makedirs(WORKSPACE_DIR)
        
        # 3. Clone the repo
        print(f"🔄 Cloning {REPO_NAME}...")
        subprocess.run(
            ['git', 'clone', REPO_URL, '.'], 
            cwd=WORKSPACE_DIR, 
            check=True, 
            capture_output=True
        )
        
        # 4. Configure Git User (Required for commits)
        subprocess.run(['git', 'config', 'user.email', 'ai_agent@bot.com'], cwd=WORKSPACE_DIR)
        subprocess.run(['git', 'config', 'user.name', 'DevOps Agent'], cwd=WORKSPACE_DIR)
        
        return f"✅ Successfully cloned {REPO_NAME} into workspace."
        
    except subprocess.CalledProcessError as e:
        return f"❌ Git Clone Failed: {e}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
    
def read_repo_file(relative_path: str):
    """
    Reads the content of a file from the cloned repository.
    Input: relative_path (e.g., 'src/revenue_engine.py')
    """
    full_path = os.path.join(WORKSPACE_DIR, relative_path)
    
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ Error: File '{relative_path}' not found."
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

def create_or_update_file(relative_path: str, content: str):
    """
    Creates a new file or overwrites an existing one in the repo.
    Useful for creating test files (tests/test_fix.py) or fixing code.
    Input: relative_path, content
    """
    full_path = os.path.join(WORKSPACE_DIR, relative_path)
    
    try:
        # Ensure the directory exists (e.g., if creating 'tests/test_new.py')
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        return f"✅ Successfully wrote to '{relative_path}'"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"
    
def push_changes_to_github(commit_message: str):
    """
    Stages, Commits, and Pushes all changes to the remote GitHub repo.
    Input: commit_message (e.g., 'Fixed bug in revenue calculation')
    """
    try:
        # 1. Git Add (Stage all files)
        subprocess.run(['git', 'add', '.'], cwd=WORKSPACE_DIR, check=True)
        
        # 2. Git Commit
        # We use --allow-empty in case the agent tries to commit without changes (prevents crash)
        subprocess.run(
            ['git', 'commit', '--allow-empty', '-m', commit_message], 
            cwd=WORKSPACE_DIR, 
            check=True
        )
        
        # 3. Git Push
        print(f"🚀 Pushing to {BRANCH_NAME}...")
        subprocess.run(['git', 'push'], cwd=WORKSPACE_DIR, check=True)
        
        return f"✅ Success: Code committed and pushed with message: '{commit_message}'"
        
    except subprocess.CalledProcessError as e:
        return f"❌ Git Push Failed. Output: {e}"
    except Exception as e:
        return f"❌ Error during push: {str(e)}"
    
def list_repo_files():
    """
    Lists all files in the repository recursively.
    Ignores the .git folder to keep output clean.
    """
    file_list = []
    
    # Check if directory exists first
    if not os.path.exists(WORKSPACE_DIR):
        return "❌ Error: Workspace directory does not exist. Did you run clone_repository()?"

    # Walk through the directory tree
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip .git directory so we don't list internal git files
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            # Create a relative path (e.g., 'src/revenue_engine.py')
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, WORKSPACE_DIR)
            file_list.append(rel_path)
            
    if not file_list:
        return "📂 Repository is empty."
        
    return "📂 Repository Structure:\n" + "\n".join(file_list)

import sys

def run_pytest():
    """
    Runs all tests in the repository using pytest.
    Returns the console output (Pass/Fail).
    """
    try:
        print("🧪 Running tests...")
        
        # We run 'pytest' inside the workspace
        # We use sys.executable to ensure we use the same python environment
        result = subprocess.run(
            [sys.executable, '-m', 'pytest'], 
            cwd=WORKSPACE_DIR, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            return f"✅ TESTS PASSED:\n{result.stdout}"
        else:
            return f"❌ TESTS FAILED:\n{result.stdout}\n(Check the errors above and fix the code)"
            
    except Exception as e:
        return f"❌ Error running pytest: {str(e)}"