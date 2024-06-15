import os
from setuptools import setup
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
   README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='api_agua_interface',
    version='1.0a0',
    packages=find_packages(),

    download_url='',

    entry_points={'console_scripts': [
        'api_aguas_interface=api_aguas_interface.main:launch_streamlit_app',
        ]},
    

    install_requires=[ 
                     'requests==2.31.0', 
                     'streamlit==1.23.1'
    ],

    include_package_data=True,
    #license='MIT License',
    description="",
    zip_safe=False,

    long_description=README,
    long_description_content_type='text/markdown',

    #python_requires='>=3.8',

)