#!/usr/bin/bash

# READ TO CREATE PYTHON PACKAGE
# https://packaging.python.org/tutorials/packaging-projects/

PACKWORKDIR="/home/aromito/rpmbuild"

function create_source () {
  echo "####################"
  echo "# Creating source"
  echo "####################"
  rm -rf $PACKWORKDIR/SOURCES/*
  cd $PACKWORKDIR/SOURCES/
  git clone https://github.com/antonioromito/rhsm-api-client/
  mv $PACKWORKDIR/SOURCES/rhsm-api-client $PACKWORKDIR/SOURCES/rhsm-api-client-1.0
  rm -rf $PACKWORKDIR/SOURCES/rhsm-api-client-1.0/.git/
  cd $PACKWORKDIR/SOURCES/
  tar -cvzf rhsm-api-client-1.0.tar.gz rhsm-api-client-1.0/
}

function upload_pytest () {
  echo "####################"
  echo "# Uploading on test.pypi.org"
  echo "####################"
  cd $PACKWORKDIR/SOURCES/rhsm-api-client-1.0/
  python setup.py sdist bdist_wheel
  python -m twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
}

function clear_srpm () {
  echo "####################"
  echo "# Cleaning old SRPMS"
  echo "####################"
  rm -rf $PACKWORKDIR/SRPMS/rhsm-api-client-1.0-1.fc29.src.rpm
  rm -rf /var/lib/mock/fedora-29-x86_64/result/rhsm-api-client-1.0-1.fc29.src.rpm
}

function create_srpm () {
  echo "####################"
  echo "# Creating SRPMS"
  echo "####################"
  cp $PACKWORKDIR/SOURCES/rhsm-api-client-1.0/rhsm-api-client.spec $PACKWORKDIR/SPECS/rhsm-api-client.spec
  mock --buildsrpm --spec $PACKWORKDIR/SPECS/rhsm-api-client.spec --sources $PACKWORKDIR/SOURCES/
}

function build_rpm () {
  echo "####################"
  echo "# Builiding RPM"
  echo "####################"
  cp /var/lib/mock/fedora-29-x86_64/result/rhsm-api-client-1.0-1.fc29.src.rpm $PACKWORKDIR/SRPMS/
  mock --rebuild $PACKWORKDIR/SRPMS/rhsm-api-client-1.0-1.fc29.src.rpm
}

function copy_rpm () {
  echo "####################"
  echo "# Copying RPM"
  echo "####################"
  cp /var/lib/mock/fedora-29-x86_64/result/rhsm-api-client-1.0-1.fc29.noarch.rpm $PACKWORKDIR/RPMS/
}

create_source
#upload_pytest
clear_srpm
create_srpm
build_rpm
copy_rpm
