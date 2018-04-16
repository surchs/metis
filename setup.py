from codecs import open
from setuptools import setup


with open('README.md', encoding='utf-8') as fd:
    LONG_DESCRIPTION = fd.read()

setup(
    name='metis',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    packages=['metis'],
    url='https://github.com/surchs/metis',
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'numpy',
        'nibabel',
        'nilearn',
        'shutil',
        'scipy',
        'scikit-learn',
        'patsy'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
    ],
)