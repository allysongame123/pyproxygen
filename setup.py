import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyproxygen",
    #version="0.0.1",
    author="h0nda",
    author_email="1@1.com",
    description="Proxylist handler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/h0nde/pyproxygen",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires='>=3.6',
)