from setuptools import setup, find_packages

setup(
	name='dl-unpack',
	version='1.0',
	description='Unrar recursively with flag files for no repeats',
	author_email='pdmmichaelsen@gmail.com',
	install_requires=['patool==1.12'],
	packages=find_packages(include=['dlunpack']),
	package_dir={'dlunpack': 'dlunpack'},
	entry_points={'console_scripts' : ['dl-unpack=dlunpack.main:main']}
)