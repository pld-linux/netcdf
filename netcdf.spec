#
# Conditional build:
%bcond_without	f90		# don't build Fortran 90 interface (just builtin F77)
%bcond_without	tests		# don't perform "make check"
				# (note: tests need endoder-enabled szip)
%bcond_with	tests_net	# remote tests (Internet access required)
#
Summary:	NetCDF: Network Common Data Form
Summary(pl.UTF-8):	NetCDF: obsługa wspólnego sieciowego formatu danych
Name:		netcdf
Version:	4.1.3
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.gz
# Source0-md5:	46a40e1405df19d8cc6ddac16704b05f
Patch0:		%{name}-info.patch
Patch1:		%{name}-szip.patch
Patch2:		%{name}-f90.patch
URL:		http://www.unidata.ucar.edu/packages/netcdf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	curl-devel
%if %{with f90}
BuildRequires:	gcc-fortran >= 5:4.0
%else
BuildRequires:	gcc-g77
%endif
BuildRequires:	hdf5-devel >= 1.8.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.4
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

%description c++-devel -l pl.UTF-8
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
%patch1 -p1
%patch2 -p1

%build
cd udunits
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../libcf
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="%{rpmcppflags} -DgFortran=1"
%configure \
	FCFLAGS="%{rpmcflags}" \
	%{!?with_tests_net:--disable-dap-remote-tests} \
	--enable-cxx-4 \
	--enable-dap \
	--enable-netcdf-4 \
	--enable-shared
# --enable-cdmremote doesn't build atm. (tested on 4.1.3)
# --enable-hdf4 would cause dependency loop (hdf4 requires netcdf)
# --with-libcf refers to symbols not included in its code (nctime.c) (tested on 4.1.3)

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

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
%doc COPYRIGHT README RELEASE_NOTES man4/netcdf.html
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
%doc man4/netcdf-c.html
%attr(755,root,root) %{_bindir}/nc-config
%attr(755,root,root) %{_libdir}/libnetcdf.so
%{_libdir}/libnetcdf.la
%{_includedir}/netcdf.h
%{_pkgconfigdir}/netcdf.pc
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
%attr(755,root,root) %{_libdir}/libnetcdf_c++4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdf_c++4.so.1

%files c++-devel
%defattr(644,root,root,755)
%doc man4/netcdf-cxx.html
%attr(755,root,root) %{_libdir}/libnetcdf_c++.so
%attr(755,root,root) %{_libdir}/libnetcdf_c++4.so
%{_libdir}/libnetcdf_c++.la
%{_libdir}/libnetcdf_c++4.la
# netcdf 3
%{_includedir}/ncvalues.h
%{_includedir}/netcdf.hh
%{_includedir}/netcdfcpp.h
# netcdf 4
%{_includedir}/ncAtt.h
%{_includedir}/ncByte.h
%{_includedir}/ncChar.h
%{_includedir}/ncCheck.h
%{_includedir}/ncCompoundType.h
%{_includedir}/ncDim.h
%{_includedir}/ncDouble.h
%{_includedir}/ncEnumType.h
%{_includedir}/ncException.h
%{_includedir}/ncFile.h
%{_includedir}/ncFloat.h
%{_includedir}/ncGroup.h
%{_includedir}/ncGroupAtt.h
%{_includedir}/ncInt.h
%{_includedir}/ncInt64.h
%{_includedir}/ncOpaqueType.h
%{_includedir}/ncShort.h
%{_includedir}/ncString.h
%{_includedir}/ncType.h
%{_includedir}/ncUbyte.h
%{_includedir}/ncUint.h
%{_includedir}/ncUint64.h
%{_includedir}/ncUshort.h
%{_includedir}/ncVar.h
%{_includedir}/ncVarAtt.h
%{_includedir}/ncVlenType.h
%{_includedir}/netcdf
%{_infodir}/netcdf-cxx.info*

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf_c++.a
%{_libdir}/libnetcdf_c++4.a

%files fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdff.so.5

%files fortran-devel
%defattr(644,root,root,755)
%doc man4/netcdf-f77.html man4/netcdf-f90.html
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
