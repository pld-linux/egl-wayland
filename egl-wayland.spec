#
# Conditional build:
%bcond_with	static_libs	# static library
#
Summary:	Wayland EGL External Platform library
Summary(pl.UTF-8):	Biblioteka platformy zewnętrznej Wayland EGL
Name:		egl-wayland
Version:	1.1.16
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/NVIDIA/egl-wayland/releases
Source0:	https://github.com/NVIDIA/egl-wayland/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a41eaebfde71495b847a39ddef5c819c
Patch0:		%{name}-pc.patch
URL:		https://github.com/NVIDIA/egl-wayland
BuildRequires:	EGL-devel >= 1.5
BuildRequires:	EGL-devel < 2
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	eglexternalplatform >= 1.1
BuildRequires:	eglexternalplatform < 2
BuildRequires:	libdrm-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	wayland-devel >= 1.15
BuildRequires:	wayland-egl-devel >= 1.15
BuildRequires:	wayland-protocols >= 1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a work-in-progress implementation of a EGL External Platform
library to add client-side Wayland support to EGL on top of EGLDevice
and EGLStream families of extensions.

This library implements an EGL External Platform interface to work
along with EGL drivers that support the external platform mechanism.

%description -l pl.UTF-8
Ten pakiet zawiera będącą w trakcie tworzenia implementację biblioteki
platformy zewnętrznej EGL dodającą obsługę strony klienta Wayland do
EGL w oparciu o rodziny rozszerzeń EGLDevice i EGLStream.

Ta biblioteka implementuje interfejs EGL External Platform do
współpracy ze sterownikami EGL obsługującymi mechanizm platform
zewnętrznych.

%package devel
Summary:	Header files for Wayland EGL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Wayland EGL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	eglexternalplatform >= 1.0
Requires:	eglexternalplatform < 2

%description devel
Header files for Wayland EGL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Wayland EGL.

%package static
Summary:	Static Wayland EGL library
Summary(pl.UTF-8):	Statyczna biblioteka Wayland EGL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Wayland EGL library.

%description static -l pl.UTF-8
Statyczna biblioteka Wayland EGL.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libnvidia-egl-wayland.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnvidia-egl-wayland.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvidia-egl-wayland.so
%{_pkgconfigdir}/wayland-eglstream.pc
# protocol description
%{_datadir}/wayland-eglstream
%{_npkgconfigdir}/wayland-eglstream-protocols.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnvidia-egl-wayland.a
%endif
