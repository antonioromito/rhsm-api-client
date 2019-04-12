%global upname rhsm-api-client

%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python3 1
%else
%global with_python3 0
%endif

%if 0%{?rhel} >= 8
%global with_python2 0
%else
%global with_python2 1
%endif

Name: python-%{upname}
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
Requires: python2-requests
Requires: python2-six


%if 0%{?with_python3}
%package -n python3-%{upname}
Summary: Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python3-oauthlib
Requires:  python3-requests-oauthlib
Requires:  python3-requests
Requires:  python3-six
%endif

%prep
%setup -qn %{upname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
 %{__python3} setup.py install -O1 --skip-build --root %{buildroot}
cp -a %{buildroot}%{_bindir}/rhsm-api-client %{buildroot}%{_sbindir}/rhsm-api-client-%{python3_version}
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%clean

%files
%doc AUTHORS README.md LICENSE
%{_bindir}/rhsm-api-client
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{upname}
%doc AUTHORS README.md LICENSE
%{_bindir}/rhsm-api-client
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/rhsm
%endif

%changelog
