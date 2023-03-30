from setuptools import setup

setup(
    name='kgpt',
    version='0.1',
    py_modules=['kgpt'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        kgpt=kgpt:kgpt_script
    ''',
)