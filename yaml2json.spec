%ifarch aarch64
%global _arch aarch64
%global BuildArchitectures aarch64
%endif

%ifarch x86_64
%global _arch x86_64
%global BuildArchitectures x86_64
%endif

%define debug_package   %{nil}
%define _build_id_links none
%define _name yaml2json
%define _prefix /opt
%define _version 1.00.01
%define _rel 0
#%define _arch x86_64
%define _binaryname y2j

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
cd %{_sourcedir}/%{_name}-%{_version}/src
PATH=$PATH:/opt/go/bin go build -o %{_sourcedir}/%{_binaryname} .
strip %{_sourcedir}/%{_binaryname}

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

