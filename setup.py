from setuptools import setup, find_packages

setup(
    name="stochastic-pseudonymizer",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "cryptography",
    ],
    author="Ray Voelker",
    author_email="ray.voelker@gmail.com",
    description="A simple stochastic pseudonymizer",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chimpy-me/stochastic-pseudonymizer",
)