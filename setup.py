#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Dipanjan Kailthya",
    author_email='dipanjan.kailthya@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Running PysparkProcessor in SageMaker Pipelines example",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyspark_sagemaker_example',
    name='pyspark_sagemaker_example',
    packages=find_packages(include=['pyspark_sagemaker_example', 'pyspark_sagemaker_example.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dipanjank/pyspark_sagemaker_example',
    version='0.1.0',
    zip_safe=False,
)
