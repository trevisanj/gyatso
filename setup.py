from setuptools import setup, find_packages
from glob import glob

setup(
    name = 'gyatso',
    packages = find_packages(),
    include_package_data=True,
    version = '21.06.15.0',
    license = 'GNU GPLv3',
    platforms = 'any',
    description = 'Game development layer on top of pygame and serverlib',
    author = 'Julio Trevisan',
    author_email = 'juliotrevisan@gmail.com',
    url = 'http://github.com/trevisanj/gyatso',
    keywords= [],
    install_requires = ["pygame"],
    python_requires = '>=3',
    scripts = glob('gyatso/scripts/*.py')
)
