%global upname rhsm-api-client

%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%global		with_python3    1
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
BuildRequires:  python-devel
BuildRequires:  python-setuptools
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

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{py3_build}
popd
%endif

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{py3_install}
cp -a %{buildroot}%{_bindir}/%{upname} %{buildroot}%{_bindir}/python3-%{upname}
popd
%endif

%files -n python2-%{upname}

%exclude %{_bindir}/%{upname}
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE


%if 0%{?with_python3}

%if 0%{?fedora}
%files -n python3-%{upname}
%{_bindir}/python3-%{upname}
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/rhsm
%doc AUTHORS README.md
%license LICENSE
%endif

%if 0%{?rhel} && 0%{?rhel} >= 7
%files -n python34-%{upname}
%{_bindir}/python34-%{upname}
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/rhsm
%doc AUTHORS README.md
%license LICENSE
%endif

%endif


%changelog
* Mon Apr 15 2019 Marcin Dulak <aromito@redhat.com> - 1.0-1
- initial package
