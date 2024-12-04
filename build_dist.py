import os
import shutil
import subprocess

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
    if os.path.exists(backend_exe):
        shutil.copy2(backend_exe, os.path.join(dist_dir, 'backend.exe'))
    else:
        print("Warning: backend.exe not found!")
    
    # Copy launcher
    launcher_exe = os.path.join(base_dir, 'dist', 'Local LLM Chat.exe')
    if not os.path.exists(launcher_exe):
        # Try building it
        print("Building launcher...")
        subprocess.run(['pyinstaller', 'launcher.spec'], check=True)
    
    if os.path.exists(launcher_exe):
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
