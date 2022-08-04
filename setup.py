from setuptools import setup

with open("README.md", mode="r", encoding="utf-8") as fp:
    long_description = fp.read()


# TODO: add license
setup(
    name="dfspy",
    version="0.1.0",
    description="Distributed File System written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dani El-Ayyass, Artem Fomin",
    author_email="dayyass@yandex.ru, artfom02@gmail.com",
    url="https://github.com/silkway-ai/pydfs",
    packages=["pydfs"],
    entry_points={"console_scripts": ["pydfs = pydfs.__main__:main"]},
    install_requires=[
        "flask==2.1.2",
        "flask-restful==0.3.9",
        "flask-sqlalchemy==2.5.1",
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
