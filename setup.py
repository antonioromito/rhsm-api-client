from setuptools import setup

from rhsm import __version__ as VERSION

setup(
    name='rhsm-cli',
    version=VERSION,
    description='Red Hat Subscription Manager (RHSM) APIs client interface to collect data '
                'from your RHSM account. ',
    author='Antonio Romito',
    author_email='aromito@redhat.com',
    url='https://github.com/antonioromito/rhsm-api-client',
    license='GPLv2+',
    scripts=['rhsm-cli'],
    packages=['rhsm', 'rhsm.objects', 'rhsm.formats'],
    install_requires=['oauthlib', 'requests'],
    python_requires = '>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4'
)
