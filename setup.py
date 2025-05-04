from setuptools import setup, find_packages

setup(
    name='flipflop-api',
    version='0.1',
    packages=find_packages(), 
    install_requires=[
        'Flask',
        'rembg',
        'Pillow',
        'blinker==1.9.0',
        'click==8.1.8',
        'importlib_metadata==8.7.0',
        'itsdangerous==2.2.0',
        'Jinja2==3.1.6',
        'MarkupSafe==3.0.2',
        'Werkzeug==3.1.3',
        'zipp==3.21.0',
    ],
)
