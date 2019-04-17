from setuptools import setup

setup(
    name='rhsm-api-client',
    version='1.0',
    packages=['rhsm'],
    url='https://github.com/antonioromito/rhsm-api-client',
    license='GPLv2+',
    scripts=['rhsm-cli'],
    author='Antonio Romito',
    author_email='aromito@redhat.com',
    description='Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account. '
)
