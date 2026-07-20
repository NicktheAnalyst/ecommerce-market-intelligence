import logging
from pathlib import Path

# Create a logs directory at the root level
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure the logger format and target output file
logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)