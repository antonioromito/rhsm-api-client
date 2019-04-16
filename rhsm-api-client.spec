%global         upname          rhsm-api-client

Name:           python-%{upname}
Version:        1.0
Release:        1%{?dist}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
License:        GPLv2+

Url:            https://github.com/antonioromito/rhsm-api-client
Source0:        %{name}-%{version}.tar.gz

Group:          Applications/System
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{upname}-%{version}-%{release}-buildroot

%if 0%{?rhel} > 7 || 0%{?fedora} >= 29
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%global with_python3    1
%global with_python2    0
%endif
%if 0%{?rhel} <= 7 || 0%{?fedora} < 29
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%global with_python3    0
%global with_python2    1
%endif

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%package -n python2-%{upname}
%{?python_provide:%python_provide python2-%{upname}}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Requires:       python2-oauthlib
Requires:       python2-requests-oauthlib
Requires:       python2-six
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{upname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%package -n python3-%{upname}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Requires:       python3-oauthlib
Requires:       python3-requests-oauthlib
Requires:       python3-six
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{upname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%autosetup

%build
%if %{with python2}
%{py2_build}
%endif # with python2
%if %{with python3}
pushd %{py3dir}
%{py3_build}
popd
%endif

%install
%if %{with python2}
%{py2_install}
%endif # with python2
%if %{with python3}
pushd %{py3dir}
%{py3_install}
popd
%endif

%if %{with python2}
%files -n python2-%{upname}
%{_bindir}/%{upname}
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif # with python2

%if %{with python3}
%files -n python3-%{upname}
%{_bindir}/%{upname}
%{python3_sitelib}/rhsm
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
