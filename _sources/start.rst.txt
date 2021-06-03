.. _start:

Getting Started
===============

Installation
------------

To install the Python MOS Interface use::

   pip install mos-interface

Authentication
--------------

An MOS account is required to obtain an authentication token. 

The MOS authentication token may be obtained by logging in to the `MOS Frontend <https://mos.fuinn.ie>`_ and clicking the username in the top right corner.

The token is passed through the ``Interface()`` function documented in the :ref:`ref`. The token may be explicitly passed through in the Python function, or as is implicit in the example below, set as an environment variable.


Example
-------

An example use of the MOS Python interface::

   from mos.interface import Interface

   # Interface
   interface = Interface()
   
   # Get model by name
   model = interface.get_model_with_name('Lasso')

   # Set inputs
   model.set_interface_object('lambd', 0.1)

   assert(model.get_name() == 'Lasso')
   assert(model.get_system() == 'cvxpy')
   assert(model.get_status() == 'created')

   # Run
   model.run()

   assert(model.get_status() == 'success')
   assert(len(model.get_execution_log()) > 0)

   # Variable
   beta = model.get_variable_state('beta', 'value')
   print('coeffficients of beta are: ',beta)

   # Function
   obj = model.get_function_state('objectivefn', 'value')
   assert(isinstance(obj, float))
