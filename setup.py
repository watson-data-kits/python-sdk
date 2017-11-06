from setuptools import setup

setup(name='knowledge_kits',
      version='0.1',
      description='Python wrapper for Watson Knowledge Kits',
      url='http://github.com/stickperson/knowledge_kits_python',
      author='Joe Meissler',
      author_email='joe@us.ibm.com',
      license='MIT',
      packages=['knowledge_kits'],
      install_requires=[
          'requests>=2.18.4,<2.19.0'
      ],
      zip_safe=False)
