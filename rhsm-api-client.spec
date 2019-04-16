%global         srcname          rhsm-api-client
%global         sum              Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

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
BuildRequires:  python2-devel
BuildRequires:  python%{python3_pkgversion}-devel

%if 0%{?with_python3_other}
BuildRequires:  python%{python3_other_pkgversion}-devel
%endif


#%if 0%{?rhel} > 7 || 0%{?fedora} >= 29
#BuildRequires:  python3-devel
#BuildRequires:  python3-setuptools
#BuildRequires:  python3-rpm-macros
#%global with_python3    1
#%global with_python2    0
#%endif
#%if 0%{?rhel} <= 7 || 0%{?fedora} < 29
#BuildRequires:  python2-devel
#BuildRequires:  python2-setuptools
#BuildRequires:  python2-rpm-macros
#%global with_python3    0
#%global with_python2    1
#%endif

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%package -n python2-%{srcname}
Summary:        %{sum}
Requires:       python2-oauthlib
Requires:       python2-requests-oauthlib
Requires:       python2-six
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{sum}
Requires:       python%{python3_pkgversion}-oauthlib
Requires:       python%{python3_pkgversion}-requests-oauthlib
Requires:       python%{python3_pkgversion}-six
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-%{srcname}
Summary:        %{sum}
Requires:       python%{python3_other_pkgversion}-oauthlib
Requires:       python%{python3_other_pkgversion}-requests-oauthlib
Requires:       python%{python3_other_pkgversion}-six
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{srcname}}

%description -n python%{python3_other_pkgversion}-%{srcname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
%endif

%prep
%autosetup

%build
%py2_build
%py3_build
%py3_other_build

%install
%py3_other_install
%py3_install
%py2_install

%files -n python2-%{srcname}
%{_bindir}/%{srcname}
%{python2_sitelib}/*
#%{python2_sitelib}/rhsm
#%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif # with python2

%files -n python%{python3_pkgversion}-%{srcname}
%{_bindir}/%{srcname}
%{_bindir}/%{srcname}-%{python3_version}
%{python3_sitelib}/*
#%{python3_sitelib}/rhsm
#%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%doc AUTHORS README.md
%license LICENSE

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{srcname}
%{_bindir}/%{srcname}
%{_bindir}/%{srcname}-%{python3_other_version}
%{python3_other_sitelib}/*
%{python3_sitelib}/rhsm
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%doc AUTHORS README.md
%license LICENSE

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
