#
# Conditional build:
%bcond_without	tests		# build without tests

%define		plugin	check_tftp
Summary:	Nagios plugin to check TFTP server
Name:		nagios-plugin-%{plugin}
Version:	1.2
Release:	3
License:	GPL v2
Group:		Networking
Source0:	http://oss.isg.inf.ethz.ch/nagiosplug/download/TFTP-%{version}.tgz
# Source0-md5:	f234cf2bcf759d6e6a7128670fb03ec3
Source1:	%{plugin}.cfg
URL:		http://oss.isg.inf.ethz.ch/nagiosplug/
%{?with_tests:BuildRequires:	python}
BuildRequires:	rpm-pythonprov
Requires:	nagios-common
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	perl(utils)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check if a file can be fetched from TFTP server.

%prep
%setup -q -n TFTP-%{version}

# fix shebang
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{plugin}.py

%build
%if %{with tests}
%{__python} %{plugin}.py --version
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{plugin}.py $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
