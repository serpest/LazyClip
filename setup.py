from setuptools import setup

setup(
    name="LazyClip",
    version="0.1",
    description="Automated clip maker",
    long_description="Automated video clip maker that synchronizes image transitions with the rhythm of the audio",
    license="GNU General Public License v3.0",
    author="serpest",
    author_email="serpest@protonmail.com",
    url="https://github.com/serpest/LazyClip",
    packages=["lazyclip"],
    install_requires=["librosa", "Pillow", "moviepy"],
)
