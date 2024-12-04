import PyInstaller.__main__
import os
import sys

def build_exe():
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to your main.py
    main_script = os.path.join(script_dir, 'main.py')
    
    # Path to the output directory
    dist_dir = os.path.join(script_dir, 'dist')
    
    # Build the executable
    PyInstaller.__main__.run([
        main_script,
        '--onefile',
        '--clean',
        '--name=main',
        f'--distpath={dist_dir}',
        '--noconsole',
        '--hidden-import=uvicorn.logging',
        '--hidden-import=uvicorn.protocols',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.protocols.http',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--add-data=.env;.',
    ])

if __name__ == '__main__':
    build_exe()
