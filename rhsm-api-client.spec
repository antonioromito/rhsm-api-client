%global upname rhsm-api-client

%{!?py2_build:		%global py2_build		CFLAGS="%{optflags}" /usr/bin/python2 setup.py  build --executable="/usr/bin/python2 -s"}
%{!?py2_install:	%global py2_install		CFLAGS="%{optflags}" /usr/bin/python2 setup.py  install -O1 --skip-build --root %{buildroot}}
%{!?py3_build:		%global py3_build		CFLAGS="%{optflags}" /usr/bin/python3 setup.py  build --executable="/usr/bin/python3 -s"}
%{!?py3_install:	%global py3_install		CFLAGS="%{optflags}" /usr/bin/python3 setup.py  install -O1 --skip-build --root %{buildroot}}

%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%global		with_python3	1
%endif

Name: python2-%{upname}
Version: 1.0
Release: 1%{?dist}
Summary: Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
License: GPLv2+

Url: https://github.com/antonioromito/rhsm-api-client
Source0: %{upname}-%{version}.tar.gz

Group: Applications/System
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires: python2-oauthlib
Requires: python2-requests-oauthlib
Requires: python2-six

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%if 0%{?with_python3}
%package -n python3-%{upname}
Summary: Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python3-oauthlib
Requires:  python3-requests-oauthlib
Requires:  python3-six

%description -n python3-%{upname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%endif

%prep
%setup -qn %{upname}-%{version}

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}'

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}'
%endif # with_python3

%build
%{py2_build}
echo ">>>>>>>>>>>>>>>>>>>>>> %{__python2}"

%if 0%{?with_python3}
pushd %{py3dir}
%{py3_build}
echo ">>>>>>>>>>>>>>>>>>>>>> %{__python2}"
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{py3_install}
cp -a %{buildroot}%{_bindir}/rhsm-api-client %{buildroot}%{_bindir}/rhsm-api-client-py%{python3_version}
popd
%endif

%{py2_install}

%clean

%files
%doc AUTHORS README.md LICENSE
%{_bindir}/rhsm-api-client
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{upname}
%doc AUTHORS README.md LICENSE
%{_bindir}/rhsm-api-client-py%{python3_version}
%{python3_sitelib}/rhsm
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%endif

%changelog
