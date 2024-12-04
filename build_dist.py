import os
import shutil
import subprocess
import time

def wait_for_file_access(filepath, retries=5, delay=2):
    """
    Waits for a file to become accessible for reading.
    Args:
        filepath (str): Path to the file.
        retries (int): Number of retries.
        delay (int): Delay between retries in seconds.
    Returns:
        bool: True if file is accessible, False otherwise.
    """
    for _ in range(retries):
        if os.path.exists(filepath) and os.access(filepath, os.R_OK):
            return True
        print(f"File {filepath} is not accessible. Retrying in {delay} seconds...")
        time.sleep(delay)
    return False

def create_dist():
    # Base paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, 'dist')
    
    # Create dist directory
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Copy backend executable
    backend_exe = os.path.join(base_dir, 'backend', 'dist', 'main.exe')
    if wait_for_file_access(backend_exe):
        shutil.copy2(backend_exe, os.path.join(dist_dir, 'backend.exe'))
    else:
        print("Warning: backend.exe not found or inaccessible!")
    
    # Copy launcher
    launcher_exe = os.path.join(base_dir, 'dist', 'Local LLM Chat.exe')
    if not os.path.exists(launcher_exe):
        # Try building it
        print("Building launcher...")
        subprocess.run(['pyinstaller', 'launcher.spec'], check=True)
    
    if wait_for_file_access(launcher_exe):
        shutil.copy2(launcher_exe, os.path.join(dist_dir, 'Local LLM Chat.exe'))
    else:
        print("Error: Failed to build or find Local LLM Chat.exe!")

    # Create frontend directory and copy files
    frontend_dist = os.path.join(base_dir, 'frontend', 'dist')
    if os.path.exists(frontend_dist):
        shutil.copytree(frontend_dist, os.path.join(dist_dir, 'frontend'))
    else:
        print("Warning: frontend dist directory not found!")
    
    # Create README
    with open(os.path.join(dist_dir, 'README.txt'), 'w') as f:
        f.write("""Local LLM Chat Application
======================

Requirements:
1. LM Studio must be installed and running
2. An internet connection for the first run to download dependencies

To start the application:
1. Run 'Local LLM Chat.exe'
2. The application will automatically start the backend server
3. Your default web browser will open with the chat interface
4. Start chatting!

Note: The first launch might take a few seconds as the backend initializes.
""")

if __name__ == '__main__':
    create_dist()
