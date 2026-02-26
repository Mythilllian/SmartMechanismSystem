from setuptools import setup

setup(
    name="smartmechanismsystem",
    version="0.1.0",
    description="Python port of YAML",
    url="https://github.com/Mythilllian/SmartMechanismSystem",
    license="Unlicense",
    packages=["smartmechanismsystem"],
    install_requires=[
        "wpilib==2026.2.1.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)