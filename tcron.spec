%define name tcron
%define version 0.5.3
%define release %mkrel 4

%define major 0
%define libname %mklibname %name %major
%define libnamedevel %mklibname %name

Summary: Another cron daemon
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Patch0: %name.makefile.patch
Patch1: tcron-check-dev_rtc.patch
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

%package -n %libnamedevel
Summary: The development files from tcron
Group: Development/Other
Obsoletes: %_lib%{name}0-devel
Provides: %name-devel = %version-%release
Requires: %libname = %version-%release

%description -n %libnamedevel
Tcron integrates 'cron' with the ATX power-up capability.
It can invoke multiple cron jobs and switch the computer on
and off any number of times per day.

This package contains files need to create applications using
tcron library.

%prep
%setup -q
%patch0 -p0 -b .orig
%patch1 -p0 -b .devrtc

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

mkdir -p %buildroot%{_var}/spool/tcron

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

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README Changelog
%_sbindir/tcrond
%_bindir/*
%_initrddir/tcrond
%config(noreplace) %_sysconfdir/tcron.conf
%_libdir/tcrontab-ap
%{_var}/spool/tcron

%files -n %libname
%defattr(-,root,root)
%doc README Changelog
%_libdir/*.so.*

%files -n %libnamedevel
%defattr(-,root,root)
%doc README README.api Changelog demo
%_libdir/*.so
%_libdir/*.a
%_includedir/*.h
