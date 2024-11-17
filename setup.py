from setuptools import setup, find_packages

setup(
    name="Solutions",
    version="1.0.0",
    description="A PDF Summarizer and Question Generator application using NLP models.",
    author="Dakshyashree And Kritika",

    url="https://github.com/dakshyashree/solutions.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pdfplumber==0.7.5",
        "transformers==4.33.2",
        "torch==2.0.1",
        "tqdm==4.68.0",
        "tkintertable==1.3.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Update this based on your project's Python compatibility
    entry_points={
        "console_scripts": [
            "solutions=ui.main:main",  # Entry point for the app
        ],
    },
)
