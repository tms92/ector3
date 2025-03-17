from setuptools import setup, find_packages

# Read the README.md content for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ecotr3',
    version='0.1.0',
    author='Ecotr3 Development Team',
    author_email='contact@ecotr3.dev',  # Placeholder email
    description='An innovative command-line tool for directory structure visualization and management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tms92/ecotr3',  # Placeholder GitHub URL
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'ector3=ecotr3.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',  # Placeholder license
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=[
        # Add any external dependencies here
        # For example: 'click>=7.0',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ],
    },
    keywords='directory tree visualization management cli tool',
)