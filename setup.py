#!/usr/bin/env python3
"""
Setup script for SQL Splitter - Advanced MySQL SQL Parser
"""

import os
from setuptools import setup, find_packages

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sql-splitter',
    version='6.0.0',
    description='Advanced MySQL SQL Parser with Visualization Component Support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SQL Splitter Team',
    author_email='contact@sqlsplitter.dev',
    url='https://github.com/yourusername/sql-splitter',
    license='MIT',
    
    packages=find_packages(),
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    
    keywords='sql parser mysql visualization ast database query analysis',
    
    python_requires='>=3.7',
    
    install_requires=[
        # No external dependencies - pure Python implementation
    ],
    
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov',
            'black',
            'flake8',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-cov',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'sql-splitter=sql_splitter.core.sql_parser_ast_v6_0:main',
        ],
    },
    
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/sql-splitter/issues',
        'Source': 'https://github.com/yourusername/sql-splitter',
        'Documentation': 'https://github.com/yourusername/sql-splitter/blob/main/docs/',
    },
)
