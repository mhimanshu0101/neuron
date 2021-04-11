import os
from setuptools import find_packages, setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Lets setup neuron package configuration.
# setup method from setuptools library manages package configuration.
setup(
    name='neuron',
    description='A framework to manage communication between multiple micro service app.',
    long_description=read('README'),
    version='1.0.0',
    packeges=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False
)