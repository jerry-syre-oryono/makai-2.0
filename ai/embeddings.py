import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_query"
    )
    return result['embedding']
