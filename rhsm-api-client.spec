Summary: Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.
Name: rhsm-api-client
Version: 1.0
Release: 1%{?dist}
Group: Applications/System
Source0: %{name}-%{version}.tar.gz
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
%setup -qn %{name}-%{version}

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_datadir}
cp -rp %{buildroot}/../../BUILD/%{name}-%{version}/rhsm-api-client %{buildroot}/%{_sbindir}
cp -rp %{buildroot}/../../BUILD/%{name}-%{version}/rhsm	%{buildroot}/%{_datadir}

%clean

%files
%{_sbindir}/rhsm-api-client
%{_datadir}/rhsm

%doc AUTHORS README.md LICENSE

%changelog
