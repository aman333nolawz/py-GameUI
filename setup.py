from setuptools import setup, find_packages

VERSION = "1.0.8"
DESCRIPTION = "A simple GUI library for pygame"


def readme():
    with open("README.md", "r") as f:
        README = f.read()
    return README


# Setting up
setup(
    name="py-GameUI",
    version=VERSION,
    author="Nolawz",
    author_email="nolawz46@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme(),
    project_urls={
        "Documentation": "https://aman333nolawz.github.io/py-GameUI/",
        "Bug Tracker": "https://github.com/aman333nolawz/py-GameUI/issues",
        "Source": "https://github.com/aman333nolawz/py-GameUI/",
    },
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    install_requires=["pygame"],
    keywords=[
        "python",
        "pygame",
        "pygame gui",
        "py-GameUI",
        "gui pygame",
        "gui package for pygame",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
