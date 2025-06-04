from setuptools import setup
import os
import sys
import warnings
import subprocess

# Loosely based on NILMTK's setup.py

TRAVIS_TAG = os.environ.get('TRAVIS_TAG', '')

if TRAVIS_TAG:
    # Use the tag as version and mark as release unless 'dev' is in it
    VERSION = TRAVIS_TAG
    ISRELEASED = 'dev' not in TRAVIS_TAG
    QUALIFIER = ''
else:
    MAJOR = 0
    MINOR = 1
    MICRO = 2
    DEV = 1  # Increment for multiple dev pre-releases
    ISRELEASED = False
    VERSION = f"{MAJOR}.{MINOR}.{MICRO}"
    QUALIFIER = ''

FULLVERSION = VERSION

if not ISRELEASED and not TRAVIS_TAG:
    try:
        # Try standard git
        pipe = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE
        ).stdout
    except OSError:
        # Fallback for msysgit
        pipe = subprocess.Popen(
            ["git.cmd", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE
        ).stdout

    raw = pipe.read().strip()
    if sys.version_info[0] >= 3:
        raw = raw.decode('ascii')
    rev = raw or None

    if rev:
        FULLVERSION += f".dev{DEV}+git.{rev}"
    else:
        FULLVERSION += f".dev{DEV}"
else:
    FULLVERSION += QUALIFIER

def write_version_py(filename=None):
    content = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'nilmtk_contrib', 'version.py'
        )
    with open(filename, 'w') as fp:
        fp.write(content % (FULLVERSION, VERSION))

write_version_py()
# End of version writing

setup(
    name='nilmtk-contrib',
    version=FULLVERSION,
    packages=[
        'nilmtk_contrib',
        'nilmtk_contrib.disaggregate'
    ],
    install_requires=[
        'nilmtk @ git+https://github.com/nilmtk/nilmtk.git',
        'nilm_metadata @ git+https://github.com/nilmtk/nilm_metadata.git',
        'tensorflow>=2.12.0,<2.16.0',
        'cvxpy>=1.0.0'
    ],
    description=(
        "State-of-the-art algorithms for energy disaggregation "
        "using NILMTK's Rapid Experimentation API"
    ),
    author='NILMTK-contrib developers',
    author_email='',
    url='https://github.com/nilmtk/nilmtk-contrib',
    download_url=(
        "https://github.com/nilmtk/nilmtk-contrib/"
        "tarball/master#egg=nilmtk-contrib-dev"
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords=(
        'smartmeters power electricity energy analytics '
        'nilm disaggregation nilmtk nilmtk-contrib'
    )
)
