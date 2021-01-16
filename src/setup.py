from setuptools import setup

setup(
    name='YASMP',
    version='0.1',
    py_modules=['app'],
    entry_points={
        'console_scripts': ['app = app:run']
    },
)
