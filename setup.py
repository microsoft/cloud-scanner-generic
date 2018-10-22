from setuptools import setup, find_packages

exec(open('cloud_scanner_generic/version.py').read())
setup(name='cloud_scanner_generic',
      version=__version__,
      description='Generic utilities for scanning cloud resources',
      url='https://microsoft.github.io/cloud-scanner-generic',
      author='Microsoft',
      author_email='cscan@microsoft.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'elasticsearch',
          'PyMySQL',
          'requests'
      ])
