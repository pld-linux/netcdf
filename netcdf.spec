Summary:	NetCDF: Network Common Data Form
Summary(pl):	NetCDF: obs³uga wspólnego sieciowego formatu danych
Name:		netcdf
Version:	3.5.0
Release:	2
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.Z
# Source0-md5:	28640a40a44f982f90f5eeb15e917a1f
Patch0:		%{name}-shared.patch
Patch1:		%{name}-makefile.patch
Patch2:		%{name}-achack.patch
Patch3:		%{name}-c++.patch
URL:		http://unidata.ucar.edu/packages/netcdf/
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	gcc-g77
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a library that provides an implementation of the
interface. The netCDF library also defines a machine-independent
format for representing scientific data. Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The netCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

%description -l pl
NetCDF (Network Common Data Form) jest interfejsem dostêpu do danych
zorganizowanych w tablice. Biblioteka netCDF definiuje niezale¿ny od
maszyny format reprezentowania danych naukowych. Interfejs oraz
biblioteka pozwalaj± na tworzenie, dostêp i wspó³dzielenie danych.
NetCDF powsta³ w Unidata Program Center w Boulder, Colorado.

%package devel
Summary:	Header files for netCDF
Summary(pl):	Pliki nag³ówkowe netCDF
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for netCDF.

%description devel -l pl
Pliki nag³ówkowe do biblioteki netCDF.

%package static
Summary:	NetCDF - static libraries
Summary(pl):	Biblioteki statyczne netCDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of netCDF libraries.

%description static -l pl
Statyczne wersje bibliotek netCDF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd src

CFLAGS="%{rpmcflags} -Df2cFortran"
# too many hacks to rebuild
%configure2_13

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_mandir}}

cd src
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

# resolve man names conflict
mv -f $RPM_BUILD_ROOT%{_mandir}/man3/netcdf.3f \
	$RPM_BUILD_ROOT%{_mandir}/man3/netcdff.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc src/COMPATIBILITY src/COPYRIGHT src/README src/RELEASE_NOTES src/cxx/cxxdoc.ps src/fortran/cfortran.doc
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
