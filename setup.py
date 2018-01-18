from setuptools import setup
import sys


REQUIRED_PYTHON = (3, 6)
if sys.version_info[:2] < REQUIRED_PYTHON:
    sys.stderr.write('Python >={} is required.'.format(REQUIRED_PYTHON))
    sys.exit(1)


version = __import__('watson_data_kits').__version__
setup(name='watson_data_kits',
      version=version,
      description='Python wrapper for Watson Data Kits',
      url='https://github.com/watson-data-kits/python-sdk',
      author='Joe Meissler',
      author_email='joe@us.ibm.com',
      license='Apache License, Version 2.0',
      packages=['watson_data_kits'],
      install_requires=[
          'requests>=2.18.4,<2.19.0'
      ],
      python_requires='>=3.6',
      zip_safe=False)
