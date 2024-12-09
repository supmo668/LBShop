from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sales.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session
