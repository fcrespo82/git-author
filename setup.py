from setuptools import setup

setup(
    name="git-set-author",
    version="1.0.0",
    author="Fernando Crespo",
    author_email="fernando82@gmail.com",
    packages=[],
    entry_points="""
    [console_scripts]
    git-author=git_author:cli
    """,
    install_requires=["click", "tabulate"],
    include_package_data=True
)
