%define debug_package   %{nil}
%define _build_id_links none
%define _name nxtools
%define _prefix /opt
%define _version 1.1.2
%define _rel 1
%define _arch x86_64
%define _binaryname yaml2json

Name:       nxtools
Version:    %{_version}
Release:    %{_rel}
Summary:    Nexus Repository Management tools

Group:      Packaging tool
License:    GPL2.0
URL:        https://git.famillegratton.net:3000/devops/nxtools

Source0:    %{name}-%{_version}.tar.gz
BuildRequires: gcc
#Requires: sudo
#Obsoletes: vmman1 > 1.140

%description
Nexus Repository Management tools

%prep
%autosetup

%build
cd src
/opt/go/bin/go mod download
PATH=$PATH:/opt/go/bin CGO_ENABLED=0 /opt/go/bin/go build -trimpath -ldflags="-s -w -buildid=" -o %{_builddir}/%{name}-%{version}/%{_binaryname} .

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%install
rm -rf %{buildroot}
install -Dpm 0755 %{_builddir}/%{name}-%{version}/%{_binaryname} %{buildroot}%{_bindir}/%{_binaryname}

%post

%preun

%postun


%files
%defattr(0755,root,root,-)
%{_bindir}/%{_binaryname}


%changelog
* Fri Aug 14 2026 Binary package builder <builder@famillegratton.net> 1.1.2-1
- RPMBUILDER: pasted over old config to new
- 2nd specfile name change
- RPMBUILDER: fixed specfile name
- moved to SemVer, GO upgrade, BUILDERS scripts cleanup

* Sat Jun 21 2025 APK Builder <builder@famillegratton.net> 1.00.00-0
- new package built with tito
