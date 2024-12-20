# TODO: build with system oc?
# S3 support: AC_SEARCH_LIBS([aws_allocator_is_valid],[aws-c-common aws-cpp-sdk-s3 aws-cpp-sdk-core], ...)
#
# Conditional build:
%bcond_with	hdf4		# HDF4 read support (needs hdf built with "--disable-netcdf")
%bcond_with	pnetcdf		# parallel I/O for classic CDF files using PnetCDF
%bcond_without	tests		# unit tests (endoder-enabled szip needed)
%bcond_with	tests_net	# remote tests (Internet access required)
#
Summary:	NetCDF: Network Common Data Form
Summary(pl.UTF-8):	NetCDF: obsługa wspólnego sieciowego formatu danych
Name:		netcdf
Version:	4.9.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://downloads.unidata.ucar.edu/netcdf-c/%{version}/%{name}-c-%{version}.tar.gz
# Source0-md5:	f48ee01534365006934f0c63d4055ea0
Patch0:		size_t.patch
Patch1:		disable-bad-test.patch
URL:		https://www.unidata.ucar.edu/software/netcdf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.66
BuildRequires:	doxygen
%{?with_hdf4:BuildRequires:	hdf-devel >= 4}
BuildRequires:	hdf5-devel >= 1.10.3
BuildRequires:	libaec-szip-devel >= 1.0
%{?with_hdf4:BuildRequires:	libjpeg-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
%{?with_pnetcdf:BuildRequires:	parallel-netcdf-devel >= 1.6.0}
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
Requires:	curl-libs >= 7.66
%{?with_hdf4:Requires:	hdf >= 4}
Requires:	hdf5 >= 1.10.3
%{?with_pnetcdf:Requires:	parallel-netcdf >= 1.6.0}
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
Requires:	curl-devel >= 7.66
%{?with_hdf4:Requires:	hdf-devel >= 4}
Requires:	hdf5-devel >= 1.10.3
Requires:	libaec-szip-devel >= 1.0
%{?with_pnetcdf:Requires:	parallel-netcdf-devel >= 1.6.0}

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
%setup -q -n %{name}-c-%{version}
%patch -P 0 -p1
%ifarch %{ix86}
%patch -P 1 -p1
%endif

%if %{without tests_net}
# assumes at least 2 processors are available via MPI
%{__sed} -i '/TESTS += run_pnetcdf_test.sh/d' nc_test/Makefile.am
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%{?with_hdf4:CPPFLAGS="%{rpmcppflags} -I/usr/include/hdf"}
%configure \
	%{!?with_tests_net:--disable-dap-remote-tests} \
	--enable-dap \
	--enable-doxygen \
	%{?with_hdf4:--enable-hdf4} \
	--enable-netcdf-4 \
	%{?with_pnetcdf:--enable-pnetcdf}

# some substitutions are missing when using autotools
%{__sed} -i -e 's,@SHOW_DOXYGEN_TAG_LIST@,NO,' \
	-e 's,@CMAKE_CURRENT_BINARY_DIR@,.,' \
	-e 's,@SERVER_SIDE_SEARCH@,NO,' \
	-e 's,@NC_ENABLE_DOXYGEN_PDF_OUTPUT@,NO,' \
	docs/Doxyfile

%{__make}

%if %{with tests}
%{__make} -j1 check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnetcdf.la
# packaged in oc package
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ocprint

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README.md RELEASE_NOTES.md
%attr(755,root,root) %{_bindir}/nc4print
%attr(755,root,root) %{_bindir}/nccopy
%attr(755,root,root) %{_bindir}/ncdump
%attr(755,root,root) %{_bindir}/ncgen
%attr(755,root,root) %{_bindir}/ncgen3
%attr(755,root,root) %{_libdir}/libnetcdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdf.so.19
%{_libdir}/libnetcdf.settings
%{_mandir}/man1/nccopy.1*
%{_mandir}/man1/ncdump.1*
%{_mandir}/man1/ncgen.1*
%{_mandir}/man1/ncgen3.1*

%files devel
%defattr(644,root,root,755)
%doc docs/html/*
%attr(755,root,root) %{_bindir}/nc-config
%attr(755,root,root) %{_libdir}/libnetcdf.so
%{_includedir}/netcdf.h
%{_includedir}/netcdf_aux.h
%{_includedir}/netcdf_dispatch.h
%{_includedir}/netcdf_filter_build.h
%{_includedir}/netcdf_filter.h
%{_includedir}/netcdf_filter_hdf5_build.h
%{_includedir}/netcdf_json.h
%{_includedir}/netcdf_mem.h
%{_includedir}/netcdf_meta.h
%{?with_pnetcdf:%{_includedir}/netcdf_par.h}
%{_pkgconfigdir}/netcdf.pc
%{_mandir}/man3/netcdf.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdf.a
