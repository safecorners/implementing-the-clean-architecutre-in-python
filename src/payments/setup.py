from setuptools import find_packages, setup

setup(
    name="payments",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "injector",
        "sqlalchemy",
        "stripe",
        "requests",
        "db_infrastructure",
        "foundation",
    ],
    extras_require={"dev": ["pytest"]},
)
