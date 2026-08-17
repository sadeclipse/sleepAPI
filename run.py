import sys
import os
from pathlib import Path
import uvicorn

root_dir = Path(__file__).resolve().parent
app_dir = root_dir / "app"

if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        app_dir=str(app_dir),
        env_file=str(root_dir / ".env"),
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
