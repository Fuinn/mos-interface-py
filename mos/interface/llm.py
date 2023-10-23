import requests
import os



def llm_describe(model_text):
    content = """
    You are a helpful assistant. Please summarize and descibe the following optimization model in a single paragraph, considering who would use the model and for what problem. Do not use bullet points.
    %s
    """ %model_text

    token = os.getenv("OPENAI_API_KEY","test")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" %token
        }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "%s" %content}
        ],
        "temperature": 0.7
    }

    url = "https://api.openai.com/v1/chat/completions"
    
    return requests.post(url, headers=headers, json=data)
