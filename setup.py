from codecs import open
from os import path
from setuptools import setup, find_packages


BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stdin-tagger',
    version='1.0.0',
    description='decorate stdin with current timestamp and optional tag',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://msztolcman.github.io/stdin-tagger/',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['pytz'],
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,

    keywords='timestamp decorate tag stdin',

    entry_points={
        'console_scripts': [
            'stdin-tagger=stdin_tagger:main',
        ],
    },
)

