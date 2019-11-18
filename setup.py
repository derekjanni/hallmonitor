from setuptools import setup, find_packages

setup(
    name='hallmonitor',
    version='0.4.1',
    description='An integration testing library that runs tests from yaml configuration.',
    python_requires='~=3.6',
    packages=find_packages(),
    scripts=['hallmonitor/hallmonitor'],
    install_requires=[
        'pyyaml',
        'requests',
        'colorama',
        'apscheduler',
        'schedule'
    ]
)
