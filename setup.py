import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GenerIter",
    version="0.2.0-dev1",
    author="Thomas Jackson Park & Jeremy Pavier",
    author_email="generiter@gmx.com",
    description="A package for Generative Iterative music composition.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GridPresence/GenerIter",
    packages=setuptools.find_packages(),
    install_requires=['pydub'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['generinv=GenerIter.app.clep_inventory:main',
                            'genercat=GenerIter.app.clep_categorise:main',
                            'generiter=GenerIter.app.clep_generator:main'],
    }
)
