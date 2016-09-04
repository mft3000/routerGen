from setuptools import setup, find_packages
from pip.req import parse_requirements
import uuid

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

version = '1.0'

setup(
    name='routerGen',
    version=version,
    py_modules=[''],
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    description = 'generate cisco configs for your lab',
    author = 'Francesco Marangione',
    author_email = 'mft@mftnet.com',
    url = 'https://github.com/mft3000/routerGen', # use the URL to the github repo
    download_url = 'https://github.com/mft3000/routerGen/tarball/%s' % version,
    keywords = ['lab', 'Cisco', 'networking'],
    classifiers = [],
)