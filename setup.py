from setuptools import setup, find_packages

# python setup.py build_ext --inplace

setup(
    name="rdaei",
    version="0.1.0",
    description="Redistricting ecological inference",
    url="https://github.com/rdatools/rdaei",
    author="alecramsay",
    author_email="a73cram5ay@gmail.com",
    license="MIT",
    packages=[
        "rdaeni",
    ],
    install_requires=["rdabase"],
    zip_safe=False,
)