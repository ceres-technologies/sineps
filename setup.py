import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sineps",
    version="0.0.7",
    author="Ceres Technologies",
    author_email="infosec@sineps.io",
    description="The official Python library for the sineps API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    license=" ",
    url=" ",
    install_requires=[
        "requests>=2.24.0",
        "aiohttp>=3.6.2",
    ],
)
