import requests
import os

def openai_preliminaries(content):
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
    
    return token,headers,data,url

def llm_describe(model_text):
    content = """
    You are a helpful assistant. Please summarize and descibe the following optimization model in a single paragraph, considering who would use the model and for what problem. Do not use bullet points.
    %s
    """ %model_text

    token,headers,data,url = openai_preliminaries(content)
    
    
    return requests.post(url, headers=headers, json=data)

def llm_analyse(model_text,var_dict):
    content = """
    You are a helpful assistant. Here is an optimization model:
    %s
    Here are the model variables expressed in dictionary form:
    %s
    Please provide a one paragraph analysis of the model variables.
    """ %(model_text,str(var_dict))

    token,headers,data,url = openai_preliminaries(content)    
    
    return requests.post(url, headers=headers, json=data)
