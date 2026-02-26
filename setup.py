from setuptools import setup

setup(
    name="smartmechanismsystem",
    version="0.1.0",
    description="Python port of YAML",
    url="https://github.com/Mythilllian/SmartMechanismSystem",
    license="Unlicense",
    packages=["smartmechanismsystem"],
    install_requires=[
        "lemonlib @ git+https://github.com/FRC5113/LemonLib.git@main",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
