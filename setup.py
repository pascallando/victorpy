from setuptools import setup
import re

version = re.search(
    '^__version__\s*=\s*["\'](.*)["\']',
    open('victorpy/__init__.py').read(),
    re.M
).group(1)

setup(
    name='victorpy',
    version=version,
    description='A simple yet powerful static site generator with Python sugar',
    packages=['victorpy'],
    install_requires=['mistune', 'pygments', 'jinja2', 'pyyaml', 'flask', 'awesome-slugify'],
    package_data={'victorpy': ['actions/*', 'templates/*', 'templates/**/*']},
    url='https://github.com/pascallando/victorpy',
    author='Pascal LANDO',
    author_email='pascal.lando@u-picardie.fr',
    keywords=['static site', 'python'],
    classifiers=[
         'Environment :: Console',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 3.6',
         'Topic :: Internet :: WWW/HTTP',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'victorpy = victorpy.core:main'
        ],
    }
)

