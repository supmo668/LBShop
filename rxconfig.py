import reflex as rx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

config = rx.Config(
    app_name="sales",
    db_url=os.getenv("DATABASE_URL", "sqlite:///sales.db"),
    # frontend_port=3000,
    # backend_port=8000,
)
