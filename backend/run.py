import uvicorn
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_root))

if __name__ == "__main__":
    # Start the server
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root / "backend")]
    )
