%global         upname          rhsm-api-client
%{!?py2_build: %global py2_build %{__python2} setup.py build}
%{!?py2_install: %global py2_install %{__python2} setup.py install --skip-build --root %{buildroot}}
%{!?py3_build: %global py3_build %{__python3} setup.py build}
%{!?py3_install: %global py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%if 0%{?rhel} && 0%{?rhel} <= 7
# Disable python 3 for RHEL <= 7
%global		    with_python3    0
%global		    with_python2    1
%endif
%if 0%{?rhel} > 7 || 0%{?fedora} > 29
# Disable python 2 build by default
%global         with_python3    1
%global         with_python2    0
%endif
%if 0%{?fedora} <= 29
%global         with_python3    1
%global         with_python2    1
%endif

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
BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%if %{with python2}
%package -n python2-%{upname}
%{?python_provide:%python_provide python2-%{upname}}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
%description -n python2-%{upname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Requires:	    python
Requires:       python2-oauthlib
Requires:       python2-requests-oauthlib
Requires:       python2-six
%endif # with python2

%if 0%{?with_python3}
%package -n     python3-%{upname}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
%description -n python3-%{upname}
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Requires:	    python3
Requires:       python3-oauthlib
Requires:       python3-requests-oauthlib
Requires:       python3-six
%endif

%prep
%autosetup
#%setup -qn      %{name}-%{version}

#%if 0%{?with_python3}
#rm -rf %{py3dir}
#cp -a . %{py3dir}
#find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
#%endif

%build
%if %{with python2}
echo "############ Python2 dir: %{py2dir}"
%{py2_build}
%endif # with python2
%if %{with python3}
echo "############ Python3 dir: %{py3dir}"
#pushd %{py3dir}
%{py3_build}
#popd
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
