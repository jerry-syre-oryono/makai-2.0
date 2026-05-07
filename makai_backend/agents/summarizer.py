import google.generativeai as genai
import os

def summarize_document(document_text: str) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    prompt = f"Summarize the following document in 3-5 bullet points:\n\n{document_text}"
    response = model.generate_content(prompt)
    return response.text
