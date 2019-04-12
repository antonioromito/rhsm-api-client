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

Summary: Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Name: rhsm-api-client
Version: 1.0
Release: 1%{?dist}
Group: Applications/System
Source0: %{name}-%{version}.tar.gz
License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Url: https://github.com/antonioromito/rhsm-api-client
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires: python2-oauthlib
Requires: python2-requests-oauthlib
Requires: python2-requests
Requires: python2-six

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python3-oauthlib
Requires:  python3-requests-oauthlib
Requires:  python3-requests
Requires:  python3-six
%endif

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%setup -qn %{name}-%{version}

%build
%if 0%{?with_python2}
%{__python2} setup.py build
%endif
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python2}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%endif
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
cp -a %{buildroot}%{_bindir}/rhsm-api-client %{buildroot}%{_sbindir}/rhsm-api-client-%{python3_version}
popd
%endif


%clean

%files
%if 0%{?with_python2}
%doc AUTHORS README.md LICENSE
%{_bindir}/rhsm-api-client
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%endif
%if 0%{?with_python3}
%files
%doc AUTHORS README.md LICENSE
%{_bindir}/rhsm-api-client
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/rhsm
%endif

%changelog
