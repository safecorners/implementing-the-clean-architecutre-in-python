from setuptools import find_packages, setup

setup(
    name="web_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-injector",
        "flask-security-too",
        "bcrypt",
        "sqlalchemy",
        "web_app_models",
        "db_infrastructure",
        "main",
        "auctions",
        "foundation",
    ],
    extras_require={"dev": ["pytest"]},
)
