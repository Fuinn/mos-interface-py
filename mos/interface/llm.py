import requests

class openAI:

    def __init__(self, token):

        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" %token
        }

        self.data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "%s" "ten plus ten equals:"}
            ],
            "temperature": 0.7
        }

    def __update_headers__(self, kwargs):
        if not self.token:
            return kwargs
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers
        return kwargs

    def __update_data__(self, kwargs):
        if not self.data:
            return kwargs
        if 'json' in kwargs:
            kwargs['json'].update(self.headers)
        else:
            kwargs['json'] = self.data
        return kwargs

    
    def post(self, url, data=None, **kwargs):
        return requests.post(url, data=data, **self.__update_data__(kwargs),
                             **self.__update_headers__(kwargs))
    
