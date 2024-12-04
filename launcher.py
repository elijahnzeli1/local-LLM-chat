import os
import sys
import subprocess
import webbrowser
import time
import signal
import psutil

def is_port_in_use(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False

def main():
    # Get the directory containing the executable
    if getattr(sys, 'frozen', False):
        # Running as compiled
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Path to the backend executable
    backend_exe = os.path.join(base_path, 'backend', 'dist', 'main.exe')

    # Check if backend is already running
    if is_port_in_use(8000):
        print("Backend is already running on port 8000")
    else:
        # Start the backend
        print("Starting backend server...")
        subprocess.Popen([backend_exe], creationflags=subprocess.CREATE_NO_WINDOW)

    # Wait for backend to start
    time.sleep(2)

    # Open frontend in browser
    frontend_url = "http://localhost:5173"
    print(f"Opening {frontend_url} in your default browser...")
    webbrowser.open(frontend_url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        # Find and kill the backend process
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'main.exe':
                os.kill(proc.info['pid'], signal.SIGTERM)

if __name__ == "__main__":
    main()
