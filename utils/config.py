from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import Optional

# Load environment variables from .env
load_dotenv()

@dataclass(frozen=True)
class Settings:
    OPENAI_API: Optional[str] = os.getenv("OEPNAI_API")
    TAVILY_API: Optional[str] = os.getenv("TRAVEILT_API")

settings = Settings()

# Optional: quick validation
if not settings.OPENAI_API:
    raise ValueError("❌ Missing OEPNAI_API in .env file")

if not settings.TAVILY_API:
    raise ValueError("❌ Missing TRAVEILT_API in .env file")
