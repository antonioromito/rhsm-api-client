%global         upname          rhsm-api-client


Name:           python2-%{upname}
Version:        1.0
Release:        1%{?dist}
Summary:        Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
License:        GPLv2+

Url:            https://github.com/antonioromito/rhsm-api-client
Source0:        %{upname}-%{version}.tar.gz

Group:          Applications/System
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot


BuildRequires:	python2-devel
BuildRequires:  python2-setuptools
Requires:	    python
Requires:       python2-oauthlib
Requires:       python2-requests-oauthlib
Requires:       python2-six

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%setup -qn      %{upname}-%{version}

%build
%{py2_build}

%install
%{py2_install}

%files -n python2-%{upname}
%{_bindir}/%{upname}
%{python2_sitelib}/rhsm
%{python2_sitelib}/rhsm_api_client-%{version}-py%{python2_version}.egg-info
%doc AUTHORS README.md
%license LICENSE

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
