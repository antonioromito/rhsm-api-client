%global         upname          rhsm-api-client


Name:           python3-%{upname}
Version:        1.0
Release:        1%{?dist}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
License:        GPLv2+

Url:            https://github.com/antonioromito/rhsm-api-client
Source0:        %{upname}-%{version}.tar.gz

Group:          Applications/System
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot


BuildRequires:	python3-devel
BuildRequires:  python3-setuptools
Requires:	    python3
Requires:       python3-oauthlib
Requires:       python3-requests-oauthlib
Requires:       python3-six

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%setup -qn      %{upname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files -n python3-%{upname}
%{_bindir}/%{upname}
%{python3_sitelib}/rhsm
%{python3_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
