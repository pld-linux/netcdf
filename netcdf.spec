#
# Conditional build:
%bcond_without	tests		# don't perform "make check"
				# (note: tests need endoder-enabled szip)
%bcond_with	tests_net	# remote tests (Internet access required)
#
Summary:	NetCDF: Network Common Data Form
Summary(pl.UTF-8):	NetCDF: obsługa wspólnego sieciowego formatu danych
Name:		netcdf
Version:	4.3.2
Release:	5
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.gz
# Source0-md5:	2fd2365e1fe9685368cd6ab0ada532a0
URL:		http://www.unidata.ucar.edu/packages/netcdf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	hdf5-devel >= 1.8.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	sed >= 4.0
BuildRequires:	szip-devel >= 2.1-2
BuildRequires:	texinfo
Requires:	hdf5 >= 1.8.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a library that provides an implementation of the
interface. The netCDF library also defines a machine-independent
format for representing scientific data. Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The netCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

This package contains C library.

%description -l pl.UTF-8
NetCDF (Network Common Data Form) jest interfejsem dostępu do danych
zorganizowanych w tablice. Biblioteka netCDF definiuje niezależny od
maszyny format reprezentowania danych naukowych. Interfejs oraz
biblioteka pozwalają na tworzenie, dostęp i współdzielenie danych.
NetCDF powstał w Unidata Program Center w Boulder, Colorado.

Ten pakiet zawiera bibliotekę dla C.

%package devel
Summary:	Header files for netCDF
Summary(pl.UTF-8):	Pliki nagłówkowe netCDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel
Requires:	hdf5-devel >= 1.8.5
Requires:	szip-devel

%description devel
Header files for netCDF - C interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki netCDF - interfejs dla C.

%package static
Summary:	NetCDF - static library
Summary(pl.UTF-8):	Biblioteka statyczna netCDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of netCDF C library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki netCDF dla C.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_tests_net:--disable-dap-remote-tests} \
	--enable-dap \
	--enable-doxygen \
	--enable-netcdf-4 \
# --enable-cdmremote doesn't build atm. (tested on 4.2)
# --enable-rpc the same
# --enable-hdf4 would cause dependency loop (hdf4 requires netcdf)

# some substitutions are missing when using autotools
%{__sed} -i -e 's,@SHOW_DOXYGEN_TAG_LIST@,NO,' \
	-e 's,@CMAKE_CURRENT_BINARY_DIR@,.,' \
	man4/Doxyfile

%{__make}

%if %{with tests}
%{__make} -j1 check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README.md RELEASE_NOTES.md
%attr(755,root,root) %{_bindir}/nccopy
%attr(755,root,root) %{_bindir}/ncdump
%attr(755,root,root) %{_bindir}/ncgen
%attr(755,root,root) %{_bindir}/ncgen3
%attr(755,root,root) %{_libdir}/libnetcdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdf.so.7
%{_mandir}/man1/nccopy.1*
%{_mandir}/man1/ncdump.1*
%{_mandir}/man1/ncgen.1*
%{_mandir}/man1/ncgen3.1*

%files devel
%defattr(644,root,root,755)
%doc man4/html/*
%attr(755,root,root) %{_bindir}/nc-config
%attr(755,root,root) %{_libdir}/libnetcdf.so
%{_libdir}/libnetcdf.la
%{_includedir}/netcdf.h
%{_pkgconfigdir}/netcdf.pc
%{_mandir}/man3/netcdf.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf.a
