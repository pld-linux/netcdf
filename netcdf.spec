Summary:	NetCDF: Network Common Data Form
Summary(pl):	NetCDF: obs³uga wspólnego sieciowego formatu danych
Name:		netcdf
Version:	3.4
Release:	1
License:	BSD-like
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.Z
Patch0:		%{name}-shared.patch
URL:		http://unidata.ucar.edu/packages/netcdf/
BuildRequires:	gcc-c++
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
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files for netCDF.

%description devel -l pl
Pliki nag³ówkowe do biblioteki netCDF.

%package static
Summary:	NetCDF - static libraries
Summary(pl):	Biblioteki statyczne netCDF
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static version of netCDF libraries.

%description static -l pl
Statyczne wersje bibliotek netCDF.

%prep
%setup -q
%patch0 -p1

%build
cd src

CFLAGS="%{?debug:-O0 -g}%{!?debug:$RPM_OPT_FLAGS} -Df2cFortran"
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_mandir}}

cd src
%{__make} install prefix=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

# remove unwanted path from libtool script
cat $RPM_BUILD_ROOT%{_libdir}/libnetcdf_c++.la | \
	awk '/^dependency_libs/ { gsub("-L[ \t]*[^ \t]*/\.libs ","") } //' \
	>$RPM_BUILD_ROOT%{_libdir}/libnetcdf_c++.la.tmp
mv -f $RPM_BUILD_ROOT%{_libdir}/libnetcdf_c++.la.tmp \
	$RPM_BUILD_ROOT%{_libdir}/libnetcdf_c++.la

# resolve man names conflict
mv -f $RPM_BUILD_ROOT%{_mandir}/man3/netcdf.3f \
	$RPM_BUILD_ROOT%{_mandir}/man3/netcdff.3

gzip -9nf COMPATIBILITY README cxx/cxxdoc.ps fortran/cfortran.doc

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
%doc src/*.gz src/cxx/*.gz src/fortran/*.gz
%{_includedir}/*
%{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
