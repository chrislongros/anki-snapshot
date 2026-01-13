from setuptools import setup

setup(
    name="anki-snapshot",
    version="1.0.0",
    description="Git-based version control for Anki collections",
    author="Chris Longros",
    url="https://github.com/chrislongros/anki-snapshot",
    py_modules=["anki_snapshot"],
    entry_points={"console_scripts": ["anki-snapshot=anki_snapshot:main"]},
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
    ],
)
