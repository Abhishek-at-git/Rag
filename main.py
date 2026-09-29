from pathlib import Path

from .server import app
import uvicorn
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))


def main():
    uvicorn.run(app, port=8001, host="0.0.0.0")


if __name__ == "__main__":
    main()