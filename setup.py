
import re
from setuptools import setup

version = re.search(
  '^__version__\s*=\s*"(.*)"',
  open('xml2omekacsv/xml2omekacsv.py').read(),
  re.M
  ).group(1)

with open("README.md", "rb") as f:
  long_descr = f.read().decode("utf-8")
    
setup(
  name="xml2omekacsv",
  packages=["xml2omekacsv"],
  entry_points={"console_scripts":['xml2omekacsv=xml2omekacsv.xml2omekacsv:main']},
  version=version,
  description="Creates omeka compatible CSVs from an xml file for curatascape stories.",
  long_description=long_descr,
  author="Chris Geroux",
  author_email="chris.geroux@ace-net.ca",
  url="",
  test_suite='nose.collector',
  test_require=['nose'],
  include_package_data=True
  )