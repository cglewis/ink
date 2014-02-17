from setuptools import setup

setup(
    name='ink',
    version='0.1.1',
    packages=['ink', ],
    license='LICENSE',
    description='Easy way to index metadata and content of files in specific directories and make them easily searchable and retrievable, in a distributed environment.',
    long_description=open('README.md').read(),
    author=u'Charlie Lewis',
    author_email='charliel@lab41.org',
    entry_points={
        'console_scripts': [
            'ink = ink.cli:main',
        ]
    }
)
