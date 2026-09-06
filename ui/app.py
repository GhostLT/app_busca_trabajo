"""
AutoJob Hunter - Web Interface Entrypoint
Pure HTML5, CSS3, JavaScript and Bootstrap 5 frontend served via lightweight Flask server.
Streamlit is no longer required or used.
"""
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from ui.server import app, start_server

if __name__ == "__main__":
    start_server(port=8000, open_browser=True)