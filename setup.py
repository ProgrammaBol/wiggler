from setuptools import setup, find_packages

setup(
    name='wiggler',
    version='0.1',
    description=("A Python IDE that uses PyGame, wxPython and jinja2 to"
                 "bring Scratch-like features to Python"),
    long_description=("A Python module that uses PyGame, wxPython and"
                      "jinja2 to bring Scratch-like features to Python."
                      "PyGame ISrequired for this module to work along"
                      "with wxPython and jinja2."),
    url='https://github.com/ProgrammaBol/wiggler',
    author='ProgrammaBol team',
    author_email='info@programmabol.it',
    license='GPLv3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='scratch pygame',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wiggler=wiggler.core.app:main',
        ],
    },
    include_package_data=True,
)
