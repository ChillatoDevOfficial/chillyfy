from setuptools import setup, find_packages

setup(
    name="chillyfy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'discord.py[voice]',
        'yt-dlp',
        'PyNaCl',
    ],
    author="ChillatoDev",
    author_email="voipfra303@gmail.com",
    description="Una libreria per creare bot musicali su Discord",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ChillatoDevOfficial/chillyfy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)