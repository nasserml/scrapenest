from setuptools import setup, find_packages

setup(
    name="scrapenest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.11.1',
        'requests>=2.28.1',
        'fake-useragent>=1.1.3',
    ],
    author="naserml",
    author_email='mnasserone@gmail.com',
    description="Intelligent web crawling with content nesting",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
    python_requires='>=3.6',
    url="https://github.com/nasserml/scrapenest"
)