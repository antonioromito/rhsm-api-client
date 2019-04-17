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
Source0:        %{srcname}-%{version}.tar.gz

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
%setup -q -n %{srcname}-%{version}

%if 0%{?with_python2}
rm -rf %{py2dir}
cp -a . %{py2dir}
%endif

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python2}
pushd %{py2dir}
%py2_build
popd
%endif
pushd %{py3dir}
%if 0%{?with_python3}
%py3_build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%py3_install
mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
popd
%endif
%if 0%{?with_python2}
pushd %{py2dir}
%py2_install
mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
popd
%endif


%if 0%{?with_python2}
%files -n python2-%{srcname}
%{_sbindir}/rhsm-cli
%{python_sitelib}/rhsm
%{python_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
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
