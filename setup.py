from setuptools import setup, find_packages

setup(
    name='vulnhawk',
    version='1.0.0',
    author='Colly-Dev',
    description='Elite Web Application Vulnerability Scanner',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Colly-Dev/VulnHawk',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'vulnhawk=vulnhawk.vulnhawk:main',
        ],
    },
)
