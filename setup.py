from setuptools import setup

setup (name='clear_folder', version= 0.1.1, author='OLeksandr',url='https://github.com/0leksandrZahar0vi4/hw7.git', license='MIT', include_package_data=True,
    entry_points = {'consol_scripts': ['cleanfolder = clean_folder.clean_folder: main']})
