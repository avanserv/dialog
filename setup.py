from setuptools import setup, find_packages

setup(
    name="avanserv-dialog",
    version="0.1.0",
    author="Antoine VS",
    author_email="avs@avanserv.com",
    description="User-friendly API for console-based user interaction.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avanserv/dialog",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
