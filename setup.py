from setuptools import setup, find_packages

setup(
    name="lrcfilter",
    version="0.1.0",
    description="Audio analysis tool for detecting censored/explicit content and instrumental tracks",
    author="LRCFilter",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "mutagen>=1.47.0",
        "faster-whisper>=1.0.0",
        "requests>=2.31.0",
        "lyricsgenius>=1.5.0",
        "rapidfuzz>=3.6.0",
        "better-profanity>=0.7.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "lrcfilter=lrcfilter.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
