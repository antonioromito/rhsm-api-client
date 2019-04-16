%global         upname          rhsm-api-client

%if 0%{?rhel} && 0%{?rhel} <= 7
# Disable python 3 for RHEL <= 7
%global		    with_python3    0
%global		    with_python2    1
%endif
%if 0%{?rhel} > 7 || 0%{?fedora} > 29
# Disable python 2 build by default
%global         with_python3    1
%global         with_python2    0
%else
%global         with_python3    0
%global         with_python2    1
%endif

Name:           %{upname}
Version:        1.0
Release:        1%{?dist}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
License:        GPLv2+

Url:            https://github.com/antonioromito/rhsm-api-client
Source0:        %{name}-%{version}.tar.gz

Group:          Applications/System
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%if %{with python2}
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
%description -n python2-%{name}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
BuildRequires:	python2-devel
BuildRequires:  python2-setuptools
Requires:	    python
Requires:       python2-oauthlib
Requires:       python2-requests-oauthlib
Requires:       python2-six

%endif # with python2

%if 0%{?with_python3}
%package -n     python3-%{name}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
%description -n python3-%{name}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
BuildRequires:	python3-devel
BuildRequires:  python3-setuptools
Requires:	    python3
Requires:       python3-oauthlib
Requires:       python3-requests-oauthlib
Requires:       python3-six
%endif


%prep
#%autosetup
%setup -qn      %{name}-%{version}

%if 0%{?with_python2}
rm -rf %{py2dir}
cp -a . %{py2dir}
%endif # with_python2
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if %{with python2}
pushd %{py2dir}
%{py2_build}
popd
%endif # with python2
%if %{with python3}
pushd %{py3dir}
%{py3_build}
popd
%endif

%install
%if %{with python2}
pushd build-py2
%{py2_install}
popd
%endif # with python2
%if %{with python3}
pushd build-py3
%{py3_install}
popd
%endif

%if %{with python2}
%files -n python2-%{name}
%{_bindir}/%{name}
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif # with python2

%if %{with python3}
%files -n python3-%{name}
%{_bindir}/%{name}
%{python3_sitelib}/rhsm
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python3_version}.egg-info
%doc AUTHORS README.md
%license LICENSE
%endif

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
