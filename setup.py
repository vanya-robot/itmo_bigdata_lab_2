from setuptools import setup, find_packages

setup(
    name="penguin_classifier",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'fastapi'
    ],
    package_dir={'': '.'},
    python_requires='>=3.9'
)