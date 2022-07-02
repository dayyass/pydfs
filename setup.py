from setuptools import setup

with open("README.md", mode="r", encoding="utf-8") as fp:
    long_description = fp.read()


# TODO: add license
setup(
    name="pydfs",
    version="0.0.1",
    description="Distributed File System written in Python",
    long_description=long_description,
    author="Dani El-Ayyass, Artem Fomin",
    author_email="dayyass@yandex.ru",
    url="https://github.com/silkway-ai/pydfs",
    packages=["pydfs"],
    entry_points={"console_scripts": ["pydfs = pydfs.__main__:main"]},
    install_requires=[
        "flask==2.1.2",
        "flask-restful==0.3.9",
        "requests==2.28.1",
    ],
    keywords=[
        "python",
        "distributed-systems",
        "hadoop",
        "filesystem",
        "hdfs",
        "mapreduce",
    ],
)