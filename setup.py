from setuptools import setup, find_packages

setup(
    name='hallmonitor',
    version='0.3',
    description='A templating tool that creates unit tests from an arbitrary file.',
    python_requires='~=3.6',
    packages=find_packages(),
    scripts=['hallmonitor/hallmonitor'],
    install_requires=[
        'pyyaml',
        'requests',
        'apscheduler',
        'schedule'
    ]
)
