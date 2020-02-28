from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='Flint-AI',
     version='0.0.1',
     author="Anthony Kallhoff",
     author_email="kallhoffa@gmail.com",
     description="A dopamine based neural net intended to overcome local optimization for an arbitrary problem set",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/kallhoffa/Flint-AI",
     package_dir={"": "src"},
     packages=find_packages(
        where="src",
        exclude=["docs"],
     ),
     install_requires=[
        'numpy',
     ],
     entry_points={
            "console_scripts": [
                "flintai=flintai.cli.main:main"
            ]
     },
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: All Rights Reserved",
         "Operating System :: OS Independent",
     ],
 )