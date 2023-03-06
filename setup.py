from setuptools import setup

setup(
    name="git-set-author",
    version="1.0.0",
    author="Fernando Crespo",
    author_email="fernando82@gmail.com",
    packages=[],
    entry_points="""
    [console_scripts]
    gsa=git_set_author:cli
    """,
    install_requires=["click", "tabulate"]
)