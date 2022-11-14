import subprocess

from setuptools import find_packages, setup


def get_tag():
    try:
        tag = subprocess.check_output(["git", "describe", "--abbrev=0"]).decode().strip()
        return tag.replace('v','')
    except Exception:
        return '0.0.0'

setup(
    name='geolib',
    version=get_tag(),
    description='Geo Lib',
    author='Someone',
    packages= find_packages(),
    python_requires=">=3.7",
    install_requires=[
                    'osmnx',
                    'matplotlib==3.5',
                    'scikit-learn'
                    ],
)
