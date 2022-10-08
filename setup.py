from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.8"

setup(
    name='jav',
    version=VERSION,
    description='A JAV Utils',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='jav',
    author='RhythmLian',
    url="https://github.com/Rhythmicc/jav",
    license='MIT',
    packages=find_packages() + ['jav.sites'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['Qpro', 'QuickStart_Rhy', 'pyperclip', 'requests'],
    entry_points={'console_scripts': [
        'jav = jav.app:main',
    ]},
)
