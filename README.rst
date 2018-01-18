Watson Data Kits
================

Python library for `Watson Data
Kits <https://console.bluemix.net/docs/services/watson-data-kits/index.html>`_.

Installation
------------
Python 3.6 is required.

Install with either ``pip`` or ``easy_install``:

``pip install watson_data_kits``

or

``easy_install watson_data_kits``

Usage
-----

Each kit has its own class with endpoints implemented as methods of the class. Query parameters should be passed as keyword arguments. Here we use the ``TravelKit`` as an example:

.. code-block:: python

    from watson_data_kits import TravelKit


    kit = TravelKit(api_key='YOUR_API_KEY', api_url='API_URL', instance_id='INSTANCE_ID')

    # pass query parameters as keyword arguments
    params = {
        'location': '37.7749,-122.4194',
        'category': 'landmarks'
    }

    data = kit.attractions(**params)
    print(data)

See the `API reference <https://console.bluemix.net/apidocs/1787-watson-data-kits-travel#introduction>`_ for available endpoints.

Development
-----------

Requirements can be installed into a virtual environment by running ``tox -e
devenv``. Tox must be installed: ``pip install tox``. When you setup your project
this way, changes to the code are automatically updated in the virtual
environment. To activate the virtual env, run ``source venv/bin/activate``.

Create a new branch for your feature. Before pushing code, run ``tox`` to ensure
that all tests and linting passes.
