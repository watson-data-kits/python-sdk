from setuptools import setup

setup(name='watson_data_kits',
      version='0.1',
      description='Python wrapper for Watson Data Kits',
      url='https://github.com/watson-data-kits/python-sdk',
      author='Joe Meissler',
      author_email='joe@us.ibm.com',
      license='MIT',
      packages=['data_kits'],
      install_requires=[
          'requests>=2.18.4,<2.19.0'
      ],
      zip_safe=False)
