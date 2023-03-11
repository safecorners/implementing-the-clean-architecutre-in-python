from setuptools import find_packages, setup

setup(
    name="web_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-injector",
        "flask-security",
        "bcrypt",
        "sqlalchemy",
        "web_app_models",
        "db_infrastructure",
        "main",
        "auctions",
    ],
    extras_require={"dev": ["pytest"]},
)
