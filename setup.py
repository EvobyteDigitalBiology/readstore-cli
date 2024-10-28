from setuptools import setup, find_packages
from readstore_cli.__version__ import __version__

setup(
    name="readstore-cli",
    version=__version__,
    author="Jonathan Alles",
    author_email="Jonathan.Alles@evo-byte.com",
    description="ReadStore Command Line Interface (CLI) Is A Python Package For Accessing Data from the ReadStore API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EvobyteDigitalBiology/readstore-cli",
    packages=find_packages(),
    license="Commercial",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.10',
    install_requires=[
        'requests>=2.32.3',
    ],
    entry_points={
        'console_scripts': [
            'readstore = readstore_cli.readstore:main'
        ]
    },
    exclude_package_data={
        "": ["*.pyc", "*.pyo", "*~"],
    },
    include_package_data=True
)