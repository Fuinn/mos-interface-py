.. _start:

***************
Getting Started
***************

^^^^^^^^^^^^^^^
Installation
^^^^^^^^^^^^^^^

To install the MOS Interface:

``pip install setup.py``

^^^^^^^^^^^^^^^
Authentication
^^^^^^^^^^^^^^^
Authentication token.

^^^^^^^^^^^^^^^
Example
^^^^^^^^^^^^^^^


An example use of the MOS Interface Package:
::
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

