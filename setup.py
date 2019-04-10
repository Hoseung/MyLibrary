"""
setuptools.find_packages() automatically determines all the packages 
needed to run this application. Yeah!
"""

import setuptools
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


reqs = parse_requirements("requirements.txt")
#reqs = [str(ir.req) for ir in install_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
        name = "mylibrary",
        version="0.0.1",
        author="Hoseung Choi",
        author_email = "hopung@gmail.com",
        description="Reference management application for astronomers",
        long_description=long_description,
        long_description_content_type="test/markdown",
        url="https://github.com/Hoseung/MyLibrary",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Languate :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=reqs
)
