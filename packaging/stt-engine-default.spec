%define _optdir	/opt
%define _appdir	%{_optdir}/apps

Name:       stt-engine-default
Summary:    Speech To Text default engine library
Version:    0.0.15a
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Samsung Proprietary License
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: edje-bin
BuildRequires: embryo-bin
BuildRequires: gettext
BuildRequires: pkgconfig(boost)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(stt)
BuildRequires: pkgconfig(stt-engine)
BuildRequires: pkgconfig(vconf)

Requires(post): coreutils

ExclusiveArch: %arm

provides:  libn66asr.so

%description
Description: Speech To Text default engine library


####
#  Preparation 
####
%prep
%setup -q
cp %{SOURCE1001} .

####
#  Build 
####
%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%ifarch %{arm}
EXTRA_CONFIGURE_OPTIONS=" --host=arm"
%endif

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=1 \
      -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE


VERBOSE=1 make %{?jobs:-j%jobs} \
  2>&1 | sed \
  -e 's%^.*: error: .*$%\x1b[37;41m&\x1b[m%' \
  -e 's%^.*: warning: .*$%\x1b[30;43m&\x1b[m%'

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
#%post
#/sbin/ldconfig
#exit 0

####
#  Post Uninstall 
####
#%postun
#/sbin/ldconfig
#exit 0

####
#  Files in Binary Packages 
####
%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_SHARE}/voice/stt/1.0/engine/*.so
%{TZ_SYS_RO_SHARE}/voice/stt/1.0/engine-info/stt-default-info.xml
%{TZ_SYS_RO_SHARE}/license/%{name}
