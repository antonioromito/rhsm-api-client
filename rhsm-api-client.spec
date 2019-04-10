Summary: Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Name: rhsm-api-client
Version: 1.0
Release: 1%{?dist}
Group: Applications/System
Source0: https://github.com/antonioromito/rhsm-api-client
License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Url: https://github.com/antonioromito/rhsm-api-client
BuildRequires: python-devel
BuildRequires: python-six
Requires: python-oauthlib
Requires: python-requests-oauthlib
Requires: python-requests
Requires: python-six


%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%setup -q

%build
make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
%find_lang %{name} || echo 0

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_sbindir}/rhsm-api-client
%{_datadir}/%{name}
%{python_sitelib}/*
%doc AUTHORS README.md LICENSE
