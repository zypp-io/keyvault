from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fp:
    install_requires = fp.read()

setup(
    name="example-pkg-YOUR-USERNAME-HERE",  # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="author@zypp.io",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python, forecasting, data-warehouse",
    url="https://github.com/zypp/sampleproject",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={"console_scripts": ["run=package.module:do_script"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    project_urls={
        "Bug Reports": "https://github.com/zypp/sampleproject/issues",
        "Source": "https://github.com/zypp/sampleproject",
    },
)
