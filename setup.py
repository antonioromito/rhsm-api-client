from distutils.core import setup

from rhsm import __version__ as VERSION

setup(
    name='rhsm',
    version=VERSION,
    description='Red Hat Subscription Manager (RHSM) APIs client interface to collect a data '
                'from your RHSM account. ',
    author='Antonio Romito',
    author_email='aromito@redhat.com',
    url='https://github.com/antonioromito/rhsm-api-client',
    license='GPLv2+',
    scripts=['rhsm-cli'],
    packages=['rhsm', 'rhsm.objects', 'rhsm.formats']
)
