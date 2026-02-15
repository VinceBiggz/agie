"""
Setup configuration for AGIE.

Allows installation via: pip install -e .

@author: Vincent Wachira
@date: 2025-02-15
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='agie',
    version='0.1.0',
    description='AI Governance Intelligence Engine - Risk assessment for AI systems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vincent Wachira Kungu',
    author_email='wachirakungu@gmail.com',
    url='https://github.com/VinceBiggz/agie',
    license='MIT',
    
    packages=find_packages(),
    
    install_requires=[
        'anthropic>=0.39.0',
        'google-genai>=1.63.0',
        'pandas>=2.2.0',
        'pyarrow>=11.0.0',
        'click>=8.1.7',
        'rich>=13.7.0',
        'python-dotenv>=1.0.0',
    ],
    
    entry_points={
        'console_scripts': [
            'agie=src.agie:cli',
        ],
    },
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
    ],
    
    python_requires='>=3.8',
    
    keywords='ai governance iso27001 risk-assessment compliance security',
)