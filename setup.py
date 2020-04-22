from setuptools import setup, find_packages
print(find_packages())
setup(
    name='hallmonitor',
    version='0.6.2',
    description='An integration testing library that runs tests from yaml configuration.',
    python_requires='~=3.6',
    packages=['hallmonitor', 'hallmonitor/services', 'hallmonitor/resources'],
    scripts=['hallmonitor/hallmonitor'],
    install_requires=[
        'pyyaml',
        'requests',
        'colorama',
        'apscheduler',
        'schedule'
    ]
)
