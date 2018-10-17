from setuptools import setup, find_packages

setup(name='cloud_scanner_generic',
      version='0.0.1',
      description='Generic utilities for scanning cloud resources',
      url='https://microsoft.github.io/cloud-scanner-generic',
      author='Microsoft',
      author_email='tanner.barlow@microsoft.com,wallace.breza@microsoft.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'elasticsearch',
          'PyMySQL',
          'requests'
      ])
