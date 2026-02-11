from setuptools import setup, find_packages

setup(
    name="llm_guard",
    version="0.1.0",
    author="Venkat Navuru",
    description="A universal evaluation and guardrail framework for AI processes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "evaluate",
        "scikit-learn",
        "detoxify",
        "torch",
        "streamlit",
        "plotly"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)