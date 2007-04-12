%define name tcron
%define version 0.5.2
%define release %mkrel 1

%define major 0
%define libname %mklibname %name %major

Summary: Another cron daemon
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Patch0: %name.makefile.patch
License: GPL
Group: System/Servers
Url: http://tcron.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): coreutils

%description
Tcron integrates 'cron' with the ATX power-up capability.
It can invoke multiple cron jobs and switch the computer on
and off any number of times per day.

%package -n %libname
Summary: Library need by tcron
Group: System/Libraries
Provides: lib%name = %version-%release

%description -n %libname
Tcron integrates 'cron' with the ATX power-up capability.
It can invoke multiple cron jobs and switch the computer on
and off any number of times per day.

This package contains the tcron common library.

%package -n %libname-devel
Summary: The development files from tcron
Group: Development/Other
Provides: lib%name-devel = %version-%release
Provides: %name-devel = %version-%release
Requires: %libname = %version-%release

%description -n %libname-devel
Tcron integrates 'cron' with the ATX power-up capability.
It can invoke multiple cron jobs and switch the computer on
and off any number of times per day.

This package contains files need to create applications using
tcron library.

%prep
%setup -q
%patch0 -p0 -b .orig

%build
%make prefix=%_prefix TCRONTAB_AP_LIB=%_libdir 

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std prefix=%_prefix TCRONTAB_AP_LIB=%_libdir

mkdir -p %buildroot%_initrddir
mv  %buildroot/%_sysconfdir/init.d/tcrond %buildroot/%_initrddir/tcrond

(
cd %buildroot%_libdir
ln -s libtcrontab-api.so.%{major} libtcrontab-api.so
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service tcrond

%preun
%_preun_service tcrond

%pre
if [ -f %_sysconfdir/tcrontab/tcrontab.conf ]; then
    if [ ! -f %_sysconfdir/tcron.conf ]; then
        mv %_sysconfdir/tcrontab/tcrontab.conf %_sysconfdir/tcron.conf
    fi
fi

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README Changelog
%_sbindir/tcrond
%_bindir/*
%_initrddir/tcrond
%config(noreplace) %_sysconfdir/tcron.conf
%_libdir/tcrontab-ap

%files -n %libname
%defattr(-,root,root)
%doc README Changelog
%_libdir/*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%doc README README.api Changelog demo
%_libdir/*.so
%_libdir/*.a
%_includedir/*.h


