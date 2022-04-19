from setuptools import find_packages, setup

setup(
    name="pyutap",
    version="0.0.1",
    description="Python wrapper for UTAP with cppyy",
    url="http://github.com/bbkrgl/pyutap",
    author="Burak Köroğlu",
    author_email="koroglu.burak@metu.edu.tr",
    license="GPL3",
    install_requires=[
        "cppyy>=1.7.1",
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True)
