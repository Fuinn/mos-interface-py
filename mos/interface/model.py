import io
import os
import time
import json
import urllib
import numpy as np
from urllib.parse import urljoin

class Model:
    """
    MOS model class.
    """

    def __init__(self, base_url, data, requests):
        """
        MOS model class.

        Parameters
        ----------
        base_url : base API url (string)
        data : raw model data (dictionary)
        requests: requests object
        """

        self.base_url = base_url
        self.data = data
        self.requests = requests
        
    def __add_variable_states__(self, var_states):

        url = urljoin(self.base_url, 'variable-state/bulk_create/')
        r = self.requests.post(url, json=var_states)
        r.raise_for_status()

    def __add_function_states__(self, func_states):

        url = urljoin(self.base_url, 'function-state/bulk_create/')
        r = self.requests.post(url, json=func_states)
        r.raise_for_status()

    def __add_constraint_states__(self, constr_states):

        url = urljoin(self.base_url, 'constraint-state/bulk_create/')
        r = self.requests.post(url, json=constr_states)
        r.raise_for_status()

    def __add_solver_state__(self, s):

        url = urljoin(self.base_url, 'solver-state/')
        r = self.requests.post(url, json=s)
        r.raise_for_status()

    def __add_problem_state__(self, s):

        url = urljoin(self.base_url, 'problem-state/')
        r = self.requests.post(url, json=s)
        r.raise_for_status()

    def __delete_input_files__(self):

        for f in self.data['interface_files']:
            if f['type'] == 'input':
                filename = '%s%s' % (f['name'], f['extension'])
                if os.path.isfile(filename):
                    print("Deleting file '%s'" %filename)
                    os.remove(filename)

    def __delete_input_object_files__(self):

        for o in self.data['interface_objects']:
            if o['type'] == 'input':
                filename = '%s%s' % (o['name'], '.json')
                if os.path.isfile(filename):
                    print("Deleting file '%s'" %filename)
                    os.remove(filename)

    def __delete_output_files__(self):

        for f in self.data['interface_files']:
            if f['type'] == 'output':
                filename = '%s%s' %(f['name'], f['extension'])
                if os.path.isfile(filename):
                    print("Deleting file '%s'" %filename)
                    os.remove(filename)

    def __download_input_files__(self):

        for f in self.data['interface_files']:
            if f['type'] == 'input' and f['data'] is not None:
                filename = '%s%s' %(f['name'], f['extension'])
                print("Downloading file %s" %filename)
                response = self.requests.get(f['data'], stream=True)
                with open(filename, "wb") as handle:
                    for data in response.iter_content():
                        handle.write(data)

    def __download_input_object_files__(self):

        for o in self.data['interface_objects']:
            if o['type'] == 'input' and o['data'] is not None:
                filename = '%s%s' %(o['name'], '.json')
                print("Downloading file %s" %filename)
                r = self.requests.get(o['data'])
                r.raise_for_status()
                with open(filename, 'w') as f:
                    json.dump(json.loads(r.content), f)

    def __get_helper_objects__(self):
        return self.data['helper_objects']

    def __get_interface_files__(self, type=None):
        assert(type in [None, 'input', 'output'])
        return [f for f in self.data['interface_files'] if (type is None or f['type'] == type)]

    def __get_interface_objects__(self, type=None):
        assert(type in [None, 'input', 'output'])
        return [o for o in self.data['interface_objects'] if (type is None or o['type'] == type)]

    def __get_variables__(self):
        return self.data['variables']

    def __get_functions__(self):
        return self.data['functions']

    def __get_constraints__(self):
        return self.data['constraints']

    def __get_solver__(self):
        return self.data['solver']

    def __get_problem__(self):
        return self.data['problem']

    def __set_execution_log__(self, log):

        url = urljoin(self.data['url'], 'set_execution_log/')
        r = self.requests.put(url, json=log)
        r.raise_for_status()

        self.data['execution_log'] = log

    def __set_status__(self, status):

        url = urljoin(self.data['url'], 'set_status/')
        r = self.requests.put(url, json=status)
        r.raise_for_status()
        self.data['status'] = status

    def __set_var_type_and_shape__(self, v, typ, shape):

        assert(typ in ['scalar', 'array', 'hashmap'])
        assert(shape is None or isinstance(shape, list))
        v['type'] = typ
        v['shape'] = shape if shape is None else [int(x) for x in shape]
        r = self.requests.put(v['url'], json=v)
        r.raise_for_status()

    def __set_constraint_type_and_shape__(self, c, typ, shape):

        assert(typ in ['scalar', 'array', 'hashmap'])
        assert(shape is None or isinstance(shape, list))
        c['type'] = typ
        c['shape'] = shape if shape is None else [int(x) for x in shape]
        r = self.requests.put(c['url'], json=c)
        r.raise_for_status()
        
    def __set_func_type_and_shape__(self, f, typ, shape):

        assert(typ in ['scalar', 'array', 'hashmap'])
        assert(shape is None or isinstance(shape, list))
        f['type'] = typ
        f['shape'] = shape if shape is None else [int(x) for x in shape]
        r = self.requests.put(f['url'], json=f)
        r.raise_for_status()

    def __set_interface_file__(self, f, filepath):

        with open(filepath, 'rb') as data_file:
            files = {'data_file': data_file}
            f['extension'] = os.path.splitext(filepath)[-1]
            r = self.requests.put(f['url'], files=files, data=f)
            r.raise_for_status()
          
    def __set_interface_object__(self, o, data, encoder=None):

        if isinstance(data, np.ndarray) and encoder is None:
            data = data.tolist()

        json_data = json.loads(json.dumps(data, cls=encoder))
        r = self.requests.put(o['url'], json={'data': json_data})
        r.raise_for_status()

    def __set_helper_object__(self, o, data, encoder=None):

        if isinstance(data, np.ndarray) and encoder is None:
            data = data.tolist()

        json_data = json.loads(json.dumps(data, cls=encoder))
        r = self.requests.put(o['url'], json={'data': json_data})
        r.raise_for_status()

    def __write__(self, file, base_path=''):
        """
        Writes model recipe to file.

        Parameters
        ----------
        file : File object
        """

        url = urljoin(self.data['url'], 'write/')
        
        r = self.requests.get(url, params={'base_path': base_path})
        r.raise_for_status()

        recipe = json.loads(r.content)

        file.write(recipe)

    def get_id(self):
        """
        Gets model ID.

        Returns
        -------
        id : integer
        """
        return self.data['id']

    def get_owner_id(self):
        """
        Gets ID of owner.

        Returns
        -------
        id : integer
        """
        return self.data["owner"]["id"]

    def get_execution_log(self):
        """
        Gets execution log.

        Returns
        -------
        log : string
        """
        
        return self.data['execution_log']

    def get_system(self):
        """
        Gets modeling system.

        Returns
        -------
        system : string
        """
        
        return self.data['system']

    def get_status(self):
        """
        Gets solution status of model

        Returns
        -------
        status : string
        """
        
        url = urljoin(self.data['url'], 'get_status/')
        
        r = self.requests.get(url)
        r.raise_for_status()

        status = json.loads(r.content)
        self.data['status'] = status

        return status

    def get_name(self):
        """
        Gets model name.

        Returns
        -------
        name : model name (string)
        """

        return self.data['name']

    def get_description(self):
        """
        Gets model description.

        Returns
        -------
        description : model description (string)
        """
        
        return self.data['description']

    def get_source(self):
        """
        Gets model source code.

        Returns
        -------
        source : model source code (string)
        """
        
        return self.data['source']

    def get_interface_file(self, name):
        """
        Gets interface file.

        Parameters
        ----------
        name : file name (string)

        Returns
        -------
        filepath : path to interface file (string)
        """
        
        for f in self.__get_interface_files__():
            if f['name'] == name:
                break
        else:
            raise ValueError("Invalid file name")

        filename = '%s%s' %(f['name'], f['extension'])
        response = self.requests.get(f['data'], stream=True)
        with open(filename, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)
        return filename

    def get_interface_object(self, name):
        """
        Gets interface object.

        Parameters
        ----------
        name : object name (string)

        Returns
        -------
        object : interface object (Python object)
        """

        for o in self.__get_interface_objects__():
            if o['name'] == name:
                break
        else:
            raise ValueError("Invalid object name")

        url = urljoin(o['url'], 'data')
        r = self.requests.get(url)
        r.raise_for_status()
        return json.loads(r.content)

    def get_helper_object(self, name):
        """
        Gets value of any helper object

        Parameters
        ----------
        name : object name (string)

        Returns
        -------
        object : helper object (Python object)
        """

        for o in self.__get_helper_objects__():
            if o['name'] == name:
                break
        else:
            raise ValueError("Invalid object name")

        url = urljoin(o['url'], 'data')
        r = self.requests.get(url)
        r.raise_for_status()
        return json.loads(r.content)

    def get_variable_type_and_shape(self, name):
        """
        Gets variable type and shape.

        Parameters
        ----------
        name : variable name (string)

        Returns
        -------
        type : string
        shape : tuple
        """

        for v in self.__get_variables__():
            if v['name'] == name:
                break
        else:
            raise ValueError('Invalid variable')

        return v['type'], tuple(v['shape']) if v['shape'] else None

    def get_constraint_type_and_shape(self, name):
        """
        Gets constraint type and shape.

        Parameters
        ----------
        name : constraint name (string)

        Returns
        -------
        type : string
        shape : tuple
        """

        for c in self.__get_constraints__():
            if c['name'] == name:
                break
        else:
            raise ValueError('Invalid constraint')

        return c['type'], tuple(c['shape']) if c['shape'] else None

    def get_variable_state(self, name, field='all'):
        """
        Gets state of a variable, all current information stored on that variable. 
        Note currently only returns values for scalar variables.

        Parameters
        ----------
        name : variable name (string)

        Returns
        -------
        state : list
        """
        
        for v in self.__get_variables__():
            if v['name'] == name:
                break
        else:
            raise ValueError('Invalid variable')

        r = self.requests.get(v['url'])
        r.raise_for_status()
        v['type'] = json.loads(r.content)['type']

        r = self.requests.get(v['states'])
        r.raise_for_status()
        states = json.loads(r.content)

        def select(s):
            if field == 'all':
                return s
            else:
                return s[field]

        if v['type'] == 'scalar':
            return select(states[0])
        elif v['type'] == 'array':
            s = np.zeros(v['shape'])
            for ss in states:
                s[tuple(ss['index'])] = select(ss)
            return s
        elif v['type'] == 'hashmap':
            return dict([(s['index'], select(s)) for s in states])
        else:
            raise TypeError('Unknown variable type')

    def get_function_state(self, name, field='all'):
        """
        Gets state of a function, returning all current information on that function.  
        Note currently only returns values for functions with scalar outputs.

        Parameters
        ----------
        name : function name (string)

        Returns
        -------
        state : list
        """

        for f in self.__get_functions__():
            if f['name'] == name:
                break
        else:
            raise ValueError('Invalid function')

        r = self.requests.get(f['states'])
        r.raise_for_status()
        states = json.loads(r.content)

        def select(s):
            if field == 'all':
                return s
            else:
                return s[field]

        if f['type'] == 'scalar':
            return select(states[0])
        elif f['type'] == 'array':
            raise NotImplementedError()
        elif f['type'] == 'hashmap':
            return dict([(s['name'], select(s)) for s in states])
        else:
            raise TypeError('Unknown function type')

    def get_constraint_state(self, name, field='all'):
        """
        Gets state of a constraint, all current information stored on that constraint. 
        Note currently only returns values for scalar constraints.

        Parameters
        ----------
        name : variable name (string)

        Returns
        -------
        state : list
        """

        for c in self.__get_constraints__():
            if c['name'] == name:
                break
        else:
            raise ValueError('Invalid constraint')

        r = self.requests.get(c['states'])
        r.raise_for_status()
        states = json.loads(r.content)

        def select(s):
            if field == 'all':
                return s
            else:
                return s[field]

        if c['type'] == 'scalar':
            return select(states[0])
        elif c['type'] == 'array':
            s = np.zeros(c['shape'])
            for ss in states:
                s[tuple(ss['index'])] = select(ss)
            return s
        elif c['type'] == 'hashmap':
            return dict([(s['name'], select(s)) for s in states])
        else:
            raise TypeError('Unknown function type')

    def get_solver_state(self):
        """
        Gets solver state, information about solver settings 
        and performance on problem.

        Returns
        -------
        state : dict
        """

        s = self.__get_solver__()
        r = self.requests.get(s['state'])
        r.raise_for_status()
        state = json.loads(r.content)
        if not state:
            return None 
        else:
            return state[0]

    def get_problem_state(self):
        """
        Gets problem state, information about problem

        Returns
        -------
        state : dict
        """
        
        p = self.__get_problem__()
        r = self.requests.get(p['state'])
        r.raise_for_status()
        state = json.loads(r.content) 
        if not state:
            return None 
        else:
            return state[0]

    def has_interface_file(self, name):
        """
        Checks if model has an interface file of a certain name

        Parameters
        ----------
        name : filename (string)

        Returns
        -------
        has_interface_file : boolean
        """
        
        for f in self.__get_interface_files__():
            if f['name'] == name:
                return True
        else:
            return False

    def has_interface_object(self, name):
        """
        Checks if model has an interface object of a certain name

        Parameters
        ----------
        name : object name (string)

        Returns
        -------
        has_interface_object : boolean
        """
        
        for o in self.__get_interface_objects__():
            if o['name'] == name:
                return True
        else:
            return False

    def has_helper_object(self, name):
        """
        Checks if model has a helper object of a certain name

        Parameters
        ----------
        name : helper object name (string)

        Returns
        -------
        has_helper_object : boolean
        """
        
        for o in self.__get_helper_objects__():
            if o['name'] == name:
                return True
        else:
            return False

    def has_variable(self, name):
        """
        Checks if model has a variable of a certain name

        Parameters
        ----------
        name : variable name (string)

        Returns
        -------
        has_variable : boolean
        """
        
        for v in self.__get_variables__():
            if v['name'] == name:
                return True
        else:
            return False

    def has_function(self, name):
        """
        Checks if model has a function of a certain name

        Parameters
        ----------
        name : function name (string)

        Returns
        -------
        has_function : boolean
        """
        
        for f in self.__get_functions__():
            if f['name'] == name:
                return True
        else:
            return False

    def has_constraint(self, name):
        """
        Checks if model has a constraint of a certain name

        Parameters
        ----------
        name : constraint name (string)

        Returns
        -------
        has_constraint : boolean
        """
        
        for c in self.__get_constraints__():
            if c['name'] == name:
                return True
        else:
            return False

    def has_solver(self):
        """
        Checks if model has a solver defined

        Returns
        -------
        has_solver : boolean
        """
        
        return self.__get_solver__() is not None

    def has_problem(self):
        """
        Checks if model has a problem defined

        Returns
        -------
        has_variable : boolean
        """
        
        return self.__get_problem__() is not None

    def reload(self):
        """
        Reloads data
        """

        r = self.requests.get(self.data['url'])
        r.raise_for_status()

        self.data = r.json()

    def run(self, blocking=True, poll_time=1):
        """
        Runs model.

        Parameters
        ----------
        blocking : when True, blocks other actions while model status queued or running (boolean)
        poll_time : integer
        """

        url = urljoin(self.data['url'], 'run/')

        r = self.requests.post(url)
        r.raise_for_status()

        while self.get_status() in ('queued', 'running') and blocking:
            time.sleep(poll_time)

        if blocking:
            self.reload()

    def set_interface_file(self, name, filepath):
        """
        Sets model interface file (assigns filepath to name)

        Parameters
        ----------
        name : interface file name (string)
        filepath : interface file filepath (string)
        """

        for f in self.__get_interface_files__():
            if f['name'] == name:
                self.__set_interface_file__(f, filepath)
                break
        else:
            raise ValueError("Invalid file name")

    def set_interface_object(self, name, data, encoder=None):
        """
        Sets model interface object

        Parameters
        ----------
        name : interface object name (string)
        data : interface object data (Python object)
        encoder : optional specific encoder for conversion of data to JSON format
        """
        
        for o in self.__get_interface_objects__():
            if o['name'] == name:
                self.__set_interface_object__(o, data, encoder=encoder)
                break
        else:
            raise ValueError("Invalid object name")

    def show_components(self):
        """
        Prints model components to screen
        """
        
        data = self.data

        title = 'Model: {}'.format(data['name']) 

        print('')
        print(title)
        print('-'*len(title))
        print('')
        print('Input Files:')
        for f in self.__get_interface_files__(type='input'):
            print('\t{}'.format(f['name']+f['extension']))
        print('Input Objects:')
        for o in self.__get_interface_objects__(type='input'):
            print('\t{}'.format(o['name']))
        print('Helper Objects:')
        for o in self.__get_helper_objects__():
            print('\t{}'.format(o['name'])) 
        print('Variables:')
        for v in self.__get_variables__():
            print('\t{}'.format(v['name']))
        print('Functions:')
        for f in self.__get_functions__():
            print('\t{}'.format(f['name']))
        print('Constraints:')
        for c in self.__get_constraints__():
            print('\t{}'.format(c['name']))
        print('Solver:')
        print('\t{}'.format(self.__get_solver__()['name'] if self.has_solver() else None))
        print('Problem:')
        print('\t{}'.format(self.__get_problem__()['name'] if self.has_problem() else None))
        print('Output Files:')
        for f in self.__get_interface_files__(type='output'):
            print('\t{}'.format(f['name']+f['extension']))
        print('Output Objects:')
        for o in self.__get_interface_objects__(type='output'):
            if o['type'] == 'output':
                print('\t{}'.format(o['name']))

    def show_recipe(self):
        """
        Prints model recipe to screen
        """

        s = io.StringIO()
        self.__write__(s)
        print(s.getvalue())
