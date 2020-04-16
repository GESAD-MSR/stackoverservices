from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='stackoverservice',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Package for processing StackOverflow data',
    pymodules=[],
    packagedir={'':'stackoverservices'},
)