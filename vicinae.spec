Name: vicinae
Version: 0.16.11
Release: %autorelease
Summary: A focused launcher for your desktop — native, fast, extensible 

License: GPLv3
URL: https://github.com/vicinaehq/vicinae
Source0: https://github.com/vicinaehq/vicinae/archive/refs/tags/v%{version}.tar.gz

# https://docs.vicinae.com/build#build-requirements
BuildRequires: g++
BuildRequires: cmake
BuildRequires: npm
BuildRequires: ninja-build
BuildRequires: mold

BuildRequires: qt6-qtbase-devel 
BuildRequires: qt6-qtsvg-devel 
BuildRequires: qt6-qtbase-private-devel 
BuildRequires: qt6-qtwayland-devel 
BuildRequires: layer-shell-qt-devel 
BuildRequires: libqalculate-devel 
BuildRequires: minizip-devel 
BuildRequires: rapidfuzz-cpp-devel 
BuildRequires: qtkeychain-qt6-devel 
BuildRequires: openssl-devel 
BuildRequires: wayland-devel 
BuildRequires: glibc-static 
BuildRequires: libstdc++-static 
BuildRequires: zlib-devel 
BuildRequires: zlib-static 
BuildRequires: abseil-cpp-devel 
BuildRequires: protobuf-devel 
BuildRequires: cmark-gfm-devel

%description
Vicinae (pronounced "vih-SIN-ay") is a high-performance, native launcher for
your desktop — built with C++ and Qt.

It comes with a rich set of built-in modules and can be easily extended using
the Typescript SDK.

Drawing inspiration from the Raycast launcher, Vicinae provides a mostly
compatible extension API, allowing reuse of many existing Raycast extensions
with minimal modification.

Vicinae is designed for developers and power users who want fast, keyboard-first
access to common system actions.

%prep
%autosetup


%build
# vicinae overrides compile flags if CMAKE_BUILD_TYPE is not set
# Build xdgpp statically for now
# TODO: Make patch
%cmake -G Ninja -DCMAKE_BUILD_TYPE=None -DBUILD_SHARED_LIBS=OFF
%cmake_build

%install
%cmake_install

%files
%{_bindir}/vicinae
%{_prefix}/lib/systemd/user/vicinae.service
%{_datadir}/applications/vicinae.desktop
%{_datadir}/applications/vicinae-url-handler.desktop
%{_datadir}/icons/hicolor/512x512/apps/vicinae.png
%{_datadir}/vicinae/themes/*
%license LICENSE

%changelog
* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-1
- new package built with tito

%autochangelog

