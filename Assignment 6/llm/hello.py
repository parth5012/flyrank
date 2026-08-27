import pathlib
import sys 
import os
from openai import OpenAI
path = pathlib.Path(__file__).parent.parent
sys.path.append(str(path))

from config import Settings

settings = Settings()
client = OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)

response = client.chat.completions.create(
    model=settings.LLM_MODEL,
    messages=[{"role": "user", "content": "Reply with exactly the word : ready"}],
)

print(response.choices[0].message.content)
