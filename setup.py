#!/usr/bin/env python3
"""
Setup script for Puch AI + Health Buddy
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="puch-health-buddy",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered WhatsApp health assistant, fact-checker, and MCP server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/puch-health-buddy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "test": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "requests-mock>=1.9",
        ],
        "mcp": [
            "mcp>=0.9.0",
            "asyncio-mqtt>=0.11.0",
            "pydantic>=2.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "puch-health-buddy=main:main",
            "puch-mcp-server=src.puch_health_buddy.mcp.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
