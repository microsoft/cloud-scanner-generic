from setuptools import setup, find_packages

setup(name='cloud_scanner_generic',
      version='0.1',
      description='Generic utilities for scanning cloud resources',
      url='',
      author='Tanner Barlow',
      author_email='tanner.barlow12@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'elasticsearch',
          'PyMySQL',
          'requests'
      ])
