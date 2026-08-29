from openai import OpenAI
import pathlib
import sys

path = pathlib.Path(__file__).parent.parent
sys.path.append(str(path))

from config import Settings
settings = Settings()
client = OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
