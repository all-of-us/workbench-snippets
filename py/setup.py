"""A setuptools based module for PIP installation of the Terra widgets package."""

import pathlib
from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()
# Get the requirements from the requirements file
requirements = (here / 'requirements.txt').read_text(encoding='utf-8')
# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='terra-widgets',
    version='0.0.1',
    license='BSD',

    description='Terra Notebook widgets',
    long_description=long_description,
    long_description_content_type='text/markdown',

    python_requires='>=3.7',
    install_requires=requirements,
    packages=find_packages(),

    url='https://github.com/all-of-us/workbench-snippets',
    project_urls={
        'Bug Reports': 'https://github.com/all-of-us/workbench-snippets/issues',
        'Source': 'https://github.com/all-of-us/workbench-snippets/blob/master/py',
    },
)
