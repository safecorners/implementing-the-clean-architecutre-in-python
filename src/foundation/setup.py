from setuptools import find_packages, setup

setup(
    name="foundation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["injector"],
    extras_require={"dev": ["pytest"]},
)
