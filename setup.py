from setuptools import find_packages, setup
import os
import subprocess

class build_binding(build):
    def run(self):
        protoc_command = ["python3", os.path.join(src_dir, "genbinding.py")]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)
        build.run(self)

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
    include_package_data=True,
    cmdclass = {
      'build': build_binding
    },
)