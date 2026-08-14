%define debug_package   %{nil}
%define _build_id_links none
%define _name yaml2json
%define _prefix /opt
%define _version 1.1.2
%define _rel 1
#%define _arch x86_64
%define _binaryname yaml2json

Name:       yaml2json
Version:    %{_version}
Release:    %{_rel}
Summary:    YAML to JSON converter

Group:      Utils
License:    GPL2.0
URL:        https://git.famillegratton.net:3000/mainline/yaml2json.git

Source0:    %{name}-%{_version}.tar.gz
#BuildArchitectures: x86_64
BuildRequires: gcc
#Requires: sudo
#Obsoletes: vmman1 > 1.140

%description
YAML to JSON converter

%prep
%autosetup

%build
cd src
go mod download
PATH=$PATH:/opt/go/bin CGO_ENABLED=0 go build -trimpath -ldflags="-s -w -buildid=" -o %{_builddir}/%{_binaryname} .


%clean
rm -rf $RPM_BUILD_ROOT

%pre
exit 0

%install
install -Dpm 0755 %{_sourcedir}/%{_binaryname} %{buildroot}%{_bindir}/%{_binaryname}

%post

%preun

%postun

%files
%defattr(-,root,root,-)
%{_bindir}/%{_binaryname}


%changelog
* Sat Jun 21 2025 APK Builder <builder@famillegratton.net> 1.00.00-0
- new package built with tito

