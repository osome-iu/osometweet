from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

tests_require = [
    "vcrpy>=1.10.3",
]

setup(
    name="osometweet",
    version="0.1",
    description="OSoMe Twitter library for academic researches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Matthew DeVerna, Christopher Torres-Lugo, Kaicheng Yang",
    author_email="mdeverna@iu.edu, torresch@indiana.edu, yangkc@iu.edu",
    url="https://github.com/truthy/osometweet",
    project_urls={
        "Documentation": "https://github.com/truthy/osometweet",
        "Issue Tracker": "https://github.com/truthy/osometweet/issues",
        "Source Code": "https://github.com/truthy/osometweet",
    },
    download_url="https://pypi.org/project/osometweet/",
    packages=["osometweet"],
    install_requires=[
        "requests>=2.24.0",
        "requests_oauthlib>=1.3.0",
        "pause"
    ],
    tests_require=tests_require,
    python_requires=">=3.5",
)