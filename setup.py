from setuptools import setup

setup(
    name='kgpt',
    version='0.2',
    py_modules=['kgpt'],
    description='Tiny tool to use AI to generate code',
    url='https://github.com/kvfrans/kgpt',
    author='Kevin Frans',
    author_email='kevinfrans2@gmail.com',
    license='MIT',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        kgpt=kgpt:kgpt_script
    ''',
)