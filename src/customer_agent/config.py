import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    groq_api_key: str = os.environ["GROQ_API_KEY"]
    fake_api_base_url: str = os.environ["FAKE_API_BASE_URL"]
    knowledge_base_path: str = os.environ["KNOWLEDGE_BASE_PATH"]



settings = Settings()