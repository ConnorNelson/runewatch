from setuptools import setup, find_packages


setup(
    name="runewatch",
    version="0.1",
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "runewatch = runewatch.__main__:main",
        ]
    },
    install_requires=["pyshark"],
)
