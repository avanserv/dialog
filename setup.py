from setuptools import find_packages, setup


with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="avanserv-dialog",
    version="1.0.0",
    author="Antoine VS",
    author_email="avs@avanserv.com",
    description="User-friendly API for console-based user interaction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avanserv/dialog",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "inquirerpy>=0.3.4,<4",
        "rich>=12.6,<13",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
