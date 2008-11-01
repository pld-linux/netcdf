#
# Conditional build:
%bcond_without	f90	# don't build Fortran 90 interface (just builtin F77)
%bcond_without	tests	# don't perform "make check"
#
Summary:	NetCDF: Network Common Data Form
Summary(pl.UTF-8):	NetCDF: obsługa wspólnego sieciowego formatu danych
Name:		netcdf
Version:	3.6.3
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.gz
# Source0-md5:	334e9bdc010b6cd03fd6531a45fe50ad
Patch0:		%{name}-info.patch
URL:		http://www.unidata.ucar.edu/packages/netcdf/
BuildRequires:	automake
%if %{with f90}
BuildRequires:	gcc-fortran >= 5:4.0
%else
BuildRequires:	gcc-g77
%endif
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	texinfo
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

%package c++
Summary:	NetCDF - C++ library
Summary(pl.UTF-8):	Biblioteka C++ netCDF
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
NetCDF - C++ library.

%description c++ -l pl.UTF-8
Biblioteka C++ netCDF.

%package c++-devel
Summary:	Header files for netCDF C++ interface
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu C++ netCDF
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for netCDF C++ interface.

%description c++ -l pl.UTF-8
Pliki nagłówkowe interfejsu C++ netCDF.

%package c++-static
Summary:	NetCDF - C++ static library
Summary(pl.UTF-8):	Statyczna biblioteka C++ netCDF
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
NetCDF - C++ static library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka C++ netCDF.

%package fortran
Summary:	NetCDF - Fortran library
Summary(pl.UTF-8):	Biblioteka Fortranu netCDF
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	netcdf-f90

%description fortran
NetCDF - Fortran 77%{?with f90: and 90} library.

%description fortran -l pl.UTF-8
Biblioteka Fortranu 77%{?with_f90: i 90} netCDF.

%package fortran-devel
Summary:	Header files for netCDF Fortran interface
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu Fortranu netCDF
Group:		Development/Libraries
Requires:	%{name}-fortran = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
%if %{with f90}
Requires:	gcc-fortran >= 5:4.0
%else
Requires:	gcc-g77
%endif
Obsoletes:	netcdf-f90-devel

%description fortran-devel
Header files for netCDF Fortran interface.

%description fortran-devel -l pl.UTF-8
Pliki nagłówkowe interfejsu Fortranu netCDF.

%package fortran-static
Summary:	NetCDF - Fortran static library
Summary(pl.UTF-8):	Statyczna biblioteka Fortranu netCDF
Group:		Development/Libraries
Requires:	%{name}-fortran-devel = %{version}-%{release}
Obsoletes:	netcdf-f90-static

%description fortran-static
NetCDF - Fortran static library.

%description fortran-static -l pl.UTF-8
Statyczna biblioteka Fortranu netCDF.

%prep
%setup -q
%patch0 -p1

%build
# too many hacks to rebuild
cp -f /usr/share/automake/config.* .
CPPFLAGS="-DgFortran=1"
%configure \
	FCFLAGS="%{rpmcflags}" \
	--enable-shared

# make it first so separate fortran library can depend on it
%{__make} -C libsrc

%{__make} \
	libnetcdff_la_LIBADD="../f90/libnetcdff90.la ../libsrc/libnetcdf.la" \
	libnetcdf_c___la_LIBADD="../libsrc/libnetcdf.la"

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libsrc install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%post	c++-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	c++-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	fortran -p /sbin/ldconfig
%postun	fortran -p /sbin/ldconfig

%post	fortran-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	fortran-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README RELEASE_NOTES man/netcdf.html
%attr(755,root,root) %{_bindir}/ncdump
%attr(755,root,root) %{_bindir}/ncgen
%attr(755,root,root) %{_libdir}/libnetcdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdf.so.4
%{_mandir}/man1/ncdump.1*
%{_mandir}/man1/ncgen.1*

%files devel
%defattr(644,root,root,755)
%doc man/netcdf-c.html
%attr(755,root,root) %{_libdir}/libnetcdf.so
%{_libdir}/libnetcdf.la
%{_includedir}/netcdf.h
%{_mandir}/man3/netcdf.3*
%{_infodir}/netcdf.info*
%{_infodir}/netcdf-c.info*
%{_infodir}/netcdf-install.info*
%{_infodir}/netcdf-tutorial.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf.a

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdf_c++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdf_c++.so.4

%files c++-devel
%defattr(644,root,root,755)
%doc man/netcdf-cxx.html
%attr(755,root,root) %{_libdir}/libnetcdf_c++.so
%{_libdir}/libnetcdf_c++.la
%{_includedir}/ncvalues.h
%{_includedir}/netcdf.hh
%{_includedir}/netcdfcpp.h
%{_infodir}/netcdf-cxx.info*

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf_c++.a

%files fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdff.so.4

%files fortran-devel
%defattr(644,root,root,755)
%doc man/netcdf-f77.html man/netcdf-f90.html
%attr(755,root,root) %{_libdir}/libnetcdff.so
%{_libdir}/libnetcdff.la
%{_includedir}/netcdf.inc
%{_mandir}/man3/netcdf_f77.3*
%{_infodir}/netcdf-f77.info*
%if %{with f90}
%{_includedir}/netcdf.mod
%{_includedir}/typesizes.mod
%{_mandir}/man3/netcdf_f90.3*
%{_infodir}/netcdf-f90.info*
%endif

%files fortran-static
%defattr(644,root,root,755)
%{_libdir}/libnetcdff.a
