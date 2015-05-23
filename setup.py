import io
import os
import re
from glob import glob

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


setup(
    name="nameless",
    version="0.1.0",
    license="BSD",
    description="An example package. Replace this with a proper project description. Generated with https://github.com/ionelmc/cookiecutter-pylibrary",
    long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),
    author="Ionel Cristian Maries",
    author_email="contact@ionelmc.ro",
    url="https://github.com/ionelmc/python-nameless",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    extras_require={
        # eg: "rst": ["docutils>=0.11"],
    },
    entry_points={
        "console_scripts": [
            "nameless = nameless.__main__:main"
        ]
    },
)
