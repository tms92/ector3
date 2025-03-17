from setuptools import setup, find_packages

# Read version from VERSION file
with open('VERSION', 'r', encoding='utf-8') as f:
    version = f.read().strip()

# Read the README.md content for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ecotr3',
    version=version,
    author='Ecotr3 Development Team',
    author_email='contact@ecotr3.dev',
    description='An innovative command-line tool for directory structure visualization and management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tms92/ecotr3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['VERSION'],
    },
    entry_points={
        'console_scripts': [
            'ector3=ecotr3.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=[
        # External dependencies
        'pyperclip>=1.8.0',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ],
    },
    keywords='directory tree visualization management cli tool',
)