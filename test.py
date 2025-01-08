from dotenv import load_dotenv
from langchain_openai import OpenAI
import os

load_dotenv()

# Verify API key is loaded
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
print(f"API key found: {api_key[:5]}...")

# Test OpenAI integration
llm = OpenAI(temperature=0)
result = llm.invoke("Say hello!")
print(f"OpenAI response: {result}")