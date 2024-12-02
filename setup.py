from setuptools import setup, find_packages

setup(
    name='source_control_system',
    version='0.1',
    packages=find_packages(),
    install_requires=['colorama'],
    entry_points={
        'console_scripts': [
            'vcs=src.vcs:main', 
        ],
    },
)
