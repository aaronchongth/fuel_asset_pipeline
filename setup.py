from glob import glob
from setuptools import setup

package_name = 'fuel_asset_pipeline'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    py_modules=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    author='Aaron Chong',
    author_email='aaronchongth@gmail.com',
    keywords=['ignition', 'fuel'],
    classifiers=[],
    description='Scripts to help check and prepare assets to be uploaded onto Ignition Fuel',
    license='Apache License, Version 2.0',
    tests_require=[],
    scripts=[
        'fuel_asset_pipeline/copy_with_ref.py'
    ],
    entry_points={
        'console_scripts': [
            'fuel_asset_pipeline = '
            'fuel_asset_pipeline.fuel_asset_pipeline:main']
    }
)

