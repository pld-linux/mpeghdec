# ilo and mmtisobmff are upstream static-only helper libraries pulled in via
# CMake FetchContent (no network at build time in PLD), with no standalone
# shared library or other consumer - so they are vendored here as Source1/Source2
# and linked statically into libmpeghdec.so rather than packaged separately.
%define		ilover		2.0.2
%define		mmtver		1.0.4
Summary:	Fraunhofer MPEG-H 3D Audio decoder library
Summary(pl.UTF-8):	Biblioteka dekodera dźwięku Fraunhofer MPEG-H 3D Audio
Name:		mpeghdec
Version:	3.0.3
Release:	1
# Fraunhofer FDK MPEG-H Software License (source-redistributable; no patent grant)
License:	distributable, patent license required in some countries
Group:		Libraries
Source0:	https://github.com/Fraunhofer-IIS/mpeghdec/archive/r%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b7b51dedd99aeefb0d72eb5cc5e3ba7d
Source1:	https://github.com/Fraunhofer-IIS/ilo/archive/r%{ilover}/ilo-%{ilover}.tar.gz
# Source1-md5:	cbff75a47b407df6d469b4b682d0c906
Source2:	https://github.com/Fraunhofer-IIS/mmtisobmff/archive/r%{mmtver}/mmtisobmff-%{mmtver}.tar.gz
# Source2-md5:	ba89ae2bcbb98b94651415502deba5e9
Patch0:		%{name}-soname.patch
Patch1:		%{name}-x32.patch
URL:		https://github.com/Fraunhofer-IIS/mpeghdec
BuildRequires:	cmake >= 3.16
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Fraunhofer MPEG-H decoder (mpeghdec) is a decoder library for the
MPEG-H 3D Audio standard (ISO/IEC 23008-3), the audio system used by
ATSC 3.0 and other next-generation broadcast and streaming services.

%description -l pl.UTF-8
Dekoder Fraunhofera MPEG-H (mpeghdec) to biblioteka dekodera standardu
MPEG-H 3D Audio (ISO/IEC 23008-3) - systemu dźwięku używanego przez ATSC
3.0 oraz inne systemy nadawcze i streamingowe nowej generacji.

%package devel
Summary:	Header files for Fraunhofer MPEG-H decoder library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dekodera Fraunhofer MPEG-H
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Fraunhofer MPEG-H decoder library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dekodera Fraunhofer MPEG-H.

%prep
%setup -q -n %{name}-r%{version} -a1 -a2
%patch -P0 -p1
%patch -P1 -p1

%build
# relative INCLUDEDIR and LIBDIR for correct .pc
# hack DATAROOTDIR to place arch-dependent .pc file in proper place
%cmake -B build \
	-DCMAKE_INSTALL_DATAROOTDIR=%{_libdir} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DFETCHCONTENT_SOURCE_DIR_ILO=$(pwd)/ilo-r%{ilover} \
	-DFETCHCONTENT_SOURCE_DIR_MMTISOBMFF=$(pwd)/mmtisobmff-r%{mmtver} \
	-Dmpeghdec_BUILD_BINARIES=OFF

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md LICENSE.txt README.md
%{_libdir}/libmpeghdec.so.*.*.*
%ghost %{_libdir}/libmpeghdec.so.3

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmpeghdec.so
%{_includedir}/mpeghdec
%{_pkgconfigdir}/mpeghdec.pc
