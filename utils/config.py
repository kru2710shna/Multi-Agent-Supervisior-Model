from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    open_ai_key : Optional[str]= os.getenv("OEPNAI_API")
    open_ai_key : Optional[str]= os.getenv("TRAVEILT_API")

settings = Settings()