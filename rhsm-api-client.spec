%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

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
BuildRequires: gettext
BuildRequires: python-six
Requires: python-oauthlib
Requires: python-requests-oauthlib
Requires: rpm-python
Requires: tar
Requires: bzip2
Requires: xz
Requires: python-six
Requires: python-futures

%description
Red Hat Subscription Manager (RHSM) APIs client interface to collect a data from your RHSM account.

%prep
%setup -q

%build
make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}-%{version}
%defattr(-,root,root,-)
%{_sbindir}/rhsm-cli
%{python_sitelib}/*
%doc AUTHORS README.md LICENSE

%changelog
* Mon Apr 15 2019 Antonio Romito <aromito@redhat.com> - 1.0-1
- initial package
