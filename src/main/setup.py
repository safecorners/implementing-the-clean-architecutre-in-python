from setuptools import find_packages, setup

setup(
    name="main",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "injector",
        "auctions",
        "auctions_infrastructure",
        "customer_relationship",
        "db_infrastructure",
        "foundation",
        "payments",
        "processes",
        "shipping",
        "shipping_infrastructure",
        "web_app_models",
    ],
)
