from setuptools import setup, find_packages

# python setup.py build_ext --inplace

setup(
    name="rdaei",
    version="0.3.0",
    description="Redistricting ecological inference",
    url="https://github.com/rdatools/rdaei",
    author="alecramsay",
    author_email="a73cram5ay@gmail.com",
    license="MIT",
    packages=[
        "rdaei",
    ],
    install_requires=["rdabase"],
    zip_safe=False,
)
