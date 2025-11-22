"""
Setup script for Neural VST Plugin Python components.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="neural-vst-plugin",
    version="1.0.0",
    author="AutoGen Team",
    author_email="support@autogen.dev",
    description="Neural VST Plugin with AutoGen Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/autogen",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "autogen-agentchat>=0.4.0",
        "autogen-ext>=0.4.0",
        "torch>=2.0.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "onnx": ["onnxruntime>=1.16.0"],
        "onnx-gpu": ["onnxruntime-gpu>=1.16.0"],
        "audio": ["librosa>=0.10.0", "soundfile>=0.12.0"],
        "dev": ["pytest>=7.4.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
)
