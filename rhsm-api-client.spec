%global         srcname          rhsm-api-client
%global         sum              Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%if 0%{?fedora} >= 28 || 0%{?rhel} > 7
%global		    with_python3    1
%global		    with_python2    0
%else
%global		    with_python3    0
%global		    with_python2    1
%endif

Name:           python-%{srcname}
Version:        1.0
Release:        1%{?dist}
Summary:        %{sum}
License:        GPLv2+

Url:            https://github.com/antonioromito/rhsm-api-client
Source0:        %{name}-%{version}.tar.gz

Group:          Applications/System
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-buildroot
BuildRequires:  gettext
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools


%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%package -n python2-%{srcname}
Summary:        %{sum}
Requires:       python2-oauthlib
Requires:       python2-requests-oauthlib
BuildRequires:  python-six
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{sum}
Requires:       python%{python3_pkgversion}-oauthlib
Requires:       python%{python3_pkgversion}-requests-oauthlib
BuildRequires:       python%{python3_pkgversion}-six
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%autosetup

%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python2}
%py2_install
mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
%endif
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
%endif

%if 0%{?with_python2}
%files -n python2-%{srcname}
%{_sbindir}/rhsm-cli
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%{_sbindir}/rhsm-cli
%{python3_sitelib}/rhsm
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
