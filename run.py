import sys
from pathlib import Path

import uvicorn


def main() -> None:
    root = Path(__file__).resolve().parent
    # Ensure "backend" is importable regardless of CWD
    sys.path.insert(0, str(root))

    # Use import string so reload works
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=[str(root)])


if __name__ == "__main__":
    main()


