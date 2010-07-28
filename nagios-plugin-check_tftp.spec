#
# Conditional build:
%bcond_without	tests		# build without tests

%define		plugin	check_tftp
Summary:	Nagios plugin to check TFTP server
Name:		nagios-plugin-%{plugin}
Version:	1.0
Release:	2
License:	GPL v2
Group:		Networking
Source0:	http://oss.isg.inf.ethz.ch/nagiosplug/download/TFTP-%{version}.tgz
# Source0-md5:	1a6afb28509681fb1178ef38b171852f
Source1:	%{plugin}.cfg
Patch0:		optparser.patch
#Source1:	%{plugin}.cfg
URL:		http://oss.isg.inf.ethz.ch/nagiosplug/
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	perl(utils)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check if a file can be fetched from TFTP server.

%prep
%setup -q -n TFTP-%{version}
%patch0 -p1

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
%doc AUTHORS ChangeLog README VERSION
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
