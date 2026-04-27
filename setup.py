from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="budget_control",
    version="0.0.1",
    description="Budget Control for Purchase Orders, Invoices and Payments",
    author="Golden Link",
    author_email="admin@golden-link.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
