#from distutils.core import setup#, find_packages
from setuptools import setup, find_packages
import sys, os

version = '0.5'

setup(
      name='mykits',
      version=version,
      author="babykick",
      description="My own kits bag",
      url="https://github.com/babykick/easykits",
      long_description=""" """,
      classifiers=[
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      ], 
      keywords='',
      author_email='babykick@163.com',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      zip_safe=False,
      include_package_data=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
                      # -*- Entry points: -*-
                   """,
      scripts = [ # Scripts
      ],
)
