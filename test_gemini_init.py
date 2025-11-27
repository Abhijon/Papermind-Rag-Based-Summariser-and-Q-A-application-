import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

try:
    print("Initializing ChatGoogleGenerativeAI...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.3,
        convert_system_message_to_human=True
    )
    print("Initialization successful.")
except Exception as e:
    print(f"Initialization failed: {e}")
