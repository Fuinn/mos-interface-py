import os
import urllib

from .requests import Requests
from .model import Model

class Interface:
    """
    MOS interface class.

    Parameters
    ----------
    url : REST API url (string). If not provided, it is constructed from
          env vars MOS_BACKEND_HOST and MOS_BACKEND_PORT
    token : authorization token (string). If not provided, it is obtained 
            from the env var MOS_BACKEND_TOKEN.
    """

    def __init__(self, url=None, token=None):
        """
        MOS interface class.

        Parameters
        ----------
        url : REST API url (string)
        token : authorization token (string). 
        """

        # URL
        if url is None:
            host = os.getenv('MOS_BACKEND_HOST', 'localhost')
            port = os.getenv('MOS_BACKEND_PORT', '8000')
            if port == '443':
                protocol = 'https'
            else:
                protocol = 'http'
            url = '{protocol}://{host}:{port}/api/'.format(
                protocol=protocol,
                host=host,
                port=port
            )
        if url[-1] != '/':
            url += '/'

        if token is None:
            token = os.getenv('MOS_BACKEND_TOKEN')

        self.url = url
        self.requests = Requests(token)

    def delete_model_with_id(self, id):
        """ 
        Deletes model with a given id.

        Parameters
        ----------
        id : model id (string)
        """

        url = urllib.parse.urljoin(self.url, 'model/%s/' %id)
        r = self.requests.delete(url)
        r.raise_for_status()
    
    def delete_model_with_name(self, name):
        """
        Deletes model with a give name.

        Parameters
        ----------
        name : model name (string)
        """

        # Get models with name
        url = urllib.parse.urljoin(self.url, 'model/?name=%s' %name)
        r = self.requests.get(url)
        r.raise_for_status()
        models = [Model(self.url, m, self.requests) for m in r.json()]
        
        # Delete
        for m in models:
            url = urllib.parse.urljoin(self.url, 'model/%s/' %m.get_id())
            r = self.requests.delete(url)
            r.raise_for_status()
    
    def get_models(self):
        """
        Gets models.

        Returns
        -------
        models: list of dictionaries
        """

        url = urllib.parse.urljoin(self.url, 'model/')
        r = self.requests.get(url)
        r.raise_for_status()
        return r.json()
    
    def get_model_with_name(self, name):
        """
        Gets model with a given name.

        Parameters
        ----------
        name : model name (string)

        Returns
        -------
        model : Model
        """

        url = urllib.parse.urljoin(self.url, 'model/?name=%s' %name)
        r = self.requests.get(url)
        r.raise_for_status()
        models = r.json()

        if not models:
            raise ValueError('No model found with name %s' %name)
        elif len(models) > 1:
            raise ValueError('More than one model found with name %s' %name)

        return self.get_model_with_id(models[0]['id'])

    def get_model_with_id(self, id):
        """
        Gets a model associated with a given ID.

        Parameters
        ----------
        id : model ID (integer)

        Returns
        --------
        model : Model
        """

        url = urllib.parse.urljoin(self.url, 'model/%s/' %id)

        r = self.requests.get(url)
        r.raise_for_status()

        return Model(self.url, r.json(), self.requests) 

    def get_user_token(self, usr, pwd):
        """
        Gets user token.

        Parameters
        ----------
        usr : user name (string)
        owd : user password (string)

        Returns
        -------
        token : user token (string)
        """

        url = urllib.parse.urljoin(self.url, 'authenticate/')

        r = self.requests.post(url, data={
            'username': usr,
            'password': pwd
        })
        r.raise_for_status()
        return r.json()['key']

    def new_model(self, filepath, quiet=True):
        """
        Creates new model from file.

        Parameters
        ----------
        filepath : path to model file (string)
        quiet : flag (boolean)

        Returns
        -------
        model : Model
        """

        url = urllib.parse.urljoin(self.url, 'model/create_from_file/')

        with open(filepath, 'r') as source_file:

            files = {'source_file': source_file}
            r = self.requests.post(url, files=files)
            r.raise_for_status()

        result = r.json()
        if not quiet:
            print(result['log'])
        if result['model'] is None:
            raise ValueError('unabel to create model')

        return Model(self.url, result['model'], self.requests)

    def set_token(self, token):
        """
        Sets interface token.

        Parameters
        ----------
        token : user token (string)
        """

        self.requests = Requests(token)
   
