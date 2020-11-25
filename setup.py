from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os import path

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

here = path.dirname(__file__)
# Get the long description from the README file
long_description = open(path.join(here, 'README.md')).read()

setup(name="Tyre",
      version=0.1.0,
      author="Kavindu Santhusa",
      author_email="kavindusanthusa@gmail.com",
      url="https://github.com/Ksengine/Tyre/",
      description="patches for python.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='compatibility, tools, utilities, patches',
      license="MIT",
      classifiers=classifiers,
      packages=["tyre"],
      project_urls={
        'Bug Reports': 'https://github.com/Ksengine/Tyre/issues',
        'Source': 'https://github.com/Ksengine/Tyre/',
        'Docs': 'https://github.com/Ksengine/Tyre/',
    },
      )
