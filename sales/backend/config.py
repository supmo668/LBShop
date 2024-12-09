import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Clerk configuration
CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

# Ensure required environment variables are set
if not CLERK_PUBLISHABLE_KEY or not CLERK_SECRET_KEY:
    raise ValueError("Missing required Clerk environment variables")
