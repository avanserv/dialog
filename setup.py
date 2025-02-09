from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()

setup(
    name="avanserv-dialog",
    version="0.1.1",
    author="Antoine VS",
    author_email="avs@avanserv.com",
    description="User-friendly API for console-based user interaction.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avanserv/dialog",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements("requirements.txt"),  # Include requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
