from setuptools import find_packages, setup

setup(
    name="auctions_infrastructure",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "injector",
        "sqlalchemy",
        "pytz",
        "auctions",
        "foundation",
        "db_infrastructure",
    ],
    extras_require={"dev": ["pytest"]},
)
