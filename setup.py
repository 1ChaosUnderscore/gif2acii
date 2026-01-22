from setuptools import setup, find_packages

setup(
    name="giftwoascii",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow>=12.1.0"
    ],
    entry_points={
        'console_scripts': [
            'giftwoascii=giftwoascii.main:main',
        ],
    },
    author="1ChaosUnderscore",
    description="Convert Images Or GIFS into ASCII art",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/1ChaosUnderscore/gif2acii",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)