from setuptools import setup
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="activeworkflow_agent",
    version="0.1",
    description="Helper library for writing ActiveWorkflow agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Automatic Mode Labs",
    author_email="info@automaticmode.com",
    url="https://github.com/automaticmode/activeworkflow-agent-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["activeworkflow_agent"],
    extras_require={
        "test": ["pytest", "schema"],
    }
)
