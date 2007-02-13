#
# Conditional build:
%bcond_without	f90	# don't build Fortran 90 interface (just builtin F77)
#
Summary:	NetCDF: Network Common Data Form
Summary(pl.UTF-8):	NetCDF: obsługa wspólnego sieciowego formatu danych
Name:		netcdf
Version:	3.6.1
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.gz
# Source0-md5:	2fde233aefb5c226bdecd9c3265d664e
Patch0:		%{name}-shared.patch
URL:		http://www.unidata.ucar.edu/packages/netcdf/
BuildRequires:	automake
%if %{with f90}
BuildRequires:	gcc-fortran >= 5:4.0
%else
BuildRequires:	gcc-g77
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a library that provides an implementation of the
interface. The netCDF library also defines a machine-independent
format for representing scientific data. Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The netCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

This package contains C and Fortran 77 library.

%description -l pl.UTF-8
NetCDF (Network Common Data Form) jest interfejsem dostępu do danych
zorganizowanych w tablice. Biblioteka netCDF definiuje niezależny od
maszyny format reprezentowania danych naukowych. Interfejs oraz
biblioteka pozwalają na tworzenie, dostęp i współdzielenie danych.
NetCDF powstał w Unidata Program Center w Boulder, Colorado.

Ten pakiet zawiera bibliotekę dla C i Fortranu 77.

%package devel
Summary:	Header files for netCDF
Summary(pl.UTF-8):	Pliki nagłówkowe netCDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for netCDF - C and Fortran 77 interfaces.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki netCDF - interfejsy dla C i Fortranu
77.

%package static
Summary:	NetCDF - static library
Summary(pl.UTF-8):	Biblioteka statyczna netCDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of netCDF C and Fortran 77 library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki netCDF dla C i Fortranu 77.

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

%package f90
Summary:	NetCDF - Fortran 90 library
Summary(pl.UTF-8):	Biblioteka Fortranu 90 netCDF
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description f90
NetCDF - Fortran 90 library.

%description f90 -l pl.UTF-8
Biblioteka Fortranu 90 netCDF.

%package f90-devel
Summary:	Header files for netCDF Fortran 90 interface
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu Fortran 90 netCDF
Group:		Development/Libraries
Requires:	%{name}-f90 = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	gcc-fortran >= 5:4.0

%description f90-devel
Header files for netCDF Fortran 90 interface.

%description f90-devel -l pl.UTF-8
Pliki nagłówkowe interfejsu Fortran 90 netCDF.

%package f90-static
Summary:	NetCDF - Fortran 90 static library
Summary(pl.UTF-8):	Statyczna biblioteka Fortranu 90 netCDF
Group:		Development/Libraries
Requires:	%{name}-f90-devel = %{version}-%{release}

%description f90-static
NetCDF - Fortran 90 static library.

%description f90-static -l pl.UTF-8
Statyczna biblioteka Fortranu 90 netCDF.

%prep
%setup -q
%patch0 -p1

%build
cd src

# too many hacks to rebuild
cp -f /usr/share/automake/config.* .
%configure

%{__make} \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_mandir}}

%{__make} -C src install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}

# resolve man names conflicts
mv -f $RPM_BUILD_ROOT%{_mandir}/man3/netcdf.3f \
	$RPM_BUILD_ROOT%{_mandir}/man3/netcdff.3
%if %{with f90}
mv -f $RPM_BUILD_ROOT%{_mandir}/man3/netcdf.3f90 \
	$RPM_BUILD_ROOT%{_mandir}/man3/netcdf_f90.3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%post	f90 -p /sbin/ldconfig
%postun	f90 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/{COPYRIGHT,README,RELEASE_NOTES}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libnetcdf.so.*.*.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc src/fortran/cfortran.doc
%attr(755,root,root) %{_libdir}/libnetcdf.so
%{_libdir}/libnetcdf.la
%{_includedir}/netcdf.h
%{_includedir}/netcdf.inc
%{_mandir}/man3/netcdf.3*
%{_mandir}/man3/netcdff.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf.a

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdf_c++.so.*.*.*

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdf_c++.so
%{_libdir}/libnetcdf_c++.la
%{_includedir}/ncvalues.h
%{_includedir}/netcdf.hh
%{_includedir}/netcdfcpp.h

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf_c++.a

%if %{with f90}
%files f90
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdf_f90.so.*.*.*

%files f90-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetcdf_f90.so
%{_libdir}/libnetcdf_f90.la
%{_includedir}/netcdf.mod
%{_includedir}/typesizes.mod
%{_mandir}/man3/netcdf_f90.3*

%files f90-static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf_f90.a
%endif
