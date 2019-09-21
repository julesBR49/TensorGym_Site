from setuptools import find_packages, setup
from package import Package

setup(name='tensor_gymnastics',
      author="Jules",
      author_email="jbrucero@uwo.ca",
      packages=find_packages(),
      include_package_data=True,
      cmdclass={
        "package": Package
    }
)
