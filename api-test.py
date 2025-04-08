from google import genai
# dotenv
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-pro-exp-03-25", contents="Explain how AI works in a few words"
)
print(response.text)