import requests

class Requests:

    def __init__(self, token):

        self.token = token
        self.headers = {'Authorization': 'Token %s' %token}

    def __update_headers__(self, kwargs):
        if not self.token:
            return kwargs
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers
        return kwargs

    def post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, 
                             **self.__update_headers__(kwargs))
    
    def get(self, url, params=None, **kwargs):
        return requests.get(url, params=params,
                            **self.__update_headers__(kwargs))

    def put(self, url, data=None, **kwargs):
        return requests.put(url, data=data,
                            **self.__update_headers__(kwargs))
    
    def delete(self, url, **kwargs):
        return requests.delete(url,
                               **self.__update_headers__(kwargs))