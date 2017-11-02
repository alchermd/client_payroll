from setuptools import setup

setup(
    name="client_payroll",
    packages=["app"],
    install_requires=[
        "flask"
    ],
    include_package_data=True
)