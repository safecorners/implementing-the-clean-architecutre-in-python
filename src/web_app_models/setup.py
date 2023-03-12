from setuptools import find_packages, setup

setup(
    name="web_app_models",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["flask-security-too", "sqlalchemy", "db_infrastructure"],
    extra_require={"dev": ["pytest"]},
)
