%define _optdir	/opt
%define _appdir	%{_optdir}/apps

Name:       org.tizen.stt-engine-default
Summary:    Speech To Text default engine library
Version:    0.0.15a
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: pkgconfig(libtzplatform-config)

%description
Description: Speech To Text default engine library

####
#  Preparation
####
%prep
%setup -q
cp %{SOURCE1001} .

%define APP_PREFIX	%{TZ_SYS_RO_APP}/%{name}
export LD_LIBRARY_PATH=%{APP_PREFIX}/lib

%define MANIFESTDIR	%{TZ_SYS_RO_PACKAGES}

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=1 \
      -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
	  -DAPP_INSTALL_PREFIX=%{APP_PREFIX} \
	  -DAPP_MANIFESTDIR=%{MANIFESTDIR}

####
#  Build
####
%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
make %{?jobs:-j%jobs}

####
#  Installation
####
%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}%{TZ_SYS_RO_SHARE}/license
cp LICENSE %{buildroot}%{TZ_SYS_RO_SHARE}/license/%{name}

####
#  Post Install
####
%post
/sbin/ldconfig
exit 0

####
#  Post Uninstall
####
%postun
/sbin/ldconfig
exit 0

####
#  Files in Binary Packages
####
%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
#%{_libdir}/*.so*
#%{TZ_SYS_RO_SHARE}/voice/stt/1.0/engine/*.so
%{TZ_SYS_RO_SHARE}/voice/stt/1.0/engine-info/org.tizen.stt-engine-default-info.xml
%{TZ_SYS_RO_SHARE}/license/%{name}
%{APP_PREFIX}/bin/*
%{APP_PREFIX}/lib/*
%{MANIFESTDIR}/org.tizen.stt-engine-default.xml
