from setuptools import setup

setup(
    name='scout2-to-csv',
    version='1.0.0',
    packages=['s2p'],
    url='',
    license='',
    author='tlozano',
    author_email='tlozano@bishopfox.com',
    description='Parses scout2 json db into csv files for reporting',
    install_requires=['click'],
    entry_points='''
    [console_scripts]
    s2p=s2p:cli''',
)
