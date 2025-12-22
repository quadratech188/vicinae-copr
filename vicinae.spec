Name: vicinae
Version: 0.17.1
Release: 1%{?dist}
Summary: A focused launcher for your desktop — native, fast, extensible 

License: GPLv3
URL: https://github.com/vicinaehq/vicinae
Source0: https://github.com/vicinaehq/vicinae/archive/refs/tags/v%{version}.tar.gz

# https://docs.vicinae.com/build#build-requirements
BuildRequires: g++
BuildRequires: cmake
BuildRequires: npm
BuildRequires: ninja-build
BuildRequires: yq

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

VICINAE_GIT_TAG=$(yq '.release.tag' < manifest.yaml)
VICINAE_GIT_COMMIT_HASH=$(yq '.release.short_rev' < manifest.yaml)

# vicinae overrides compile flags if CMAKE_BUILD_TYPE is not set
# Build xdgpp statically for now
# TODO: Make patch
%cmake -G Ninja -DCMAKE_BUILD_TYPE=Custom -DBUILD_SHARED_LIBS=OFF \
	-DVICINAE_GIT_TAG=v%{version} \
	-DVICINAE_GIT_COMMIT_HASH=${VICINAE_GIT_COMMIT_HASH}
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
* Mon Dec 22 2025 Quadratech188 <quadratech188@gmail.com> 0.17.1-1
- chore: Bump to v0.17.1 (quadratech188@gmail.com)

* Sun Dec 21 2025 Quadratech188 <quadratech188@gmail.com> 0.17.0-1
- chore: Bump to v0.17.0 (quadratech188@gmail.com)

* Tue Dec 09 2025 Quadratech188 <quadratech188@gmail.com> 0.16.14-1
- chore: Bump to v0.16.14 (quadratech188@gmail.com)
- fix: Fix wrong version check (quadratech188@gmail.com)

* Mon Dec 08 2025 Quadratech188 <quadratech188@gmail.com> 0.16.13-1
- chore: Bump to v0.16.13 (quadratech188@gmail.com)
- feat: Finish auto update (quadratech188@gmail.com)
- chore: Make release.py executable (quadratech188@gmail.com)
- feat: Add version checking (quadratech188@gmail.com)
- fix: Reset Release number when updating (quadratech188@gmail.com)
- feat: Add release script (quadratech188@gmail.com)

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-11
- 

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-10
- fix: Use version info instead of manifest.yaml (quadratech188@gmail.com)

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-9
- Add Git information to build (quadratech188@gmail.com)

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-8
- Test autorebuild

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-7
- Test auto rebuild

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-6
- Test auto rebuild

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com>
- Test autorebuild

* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-4
- Remove mold (quadratech188@gmail.com)

* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-3
- Test auto rebuild

* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-2
- Make Release field use tito's release var (quadratech188@gmail.com)
- Embed xdgpp statically (quadratech188@gmail.com)
- Update README.md (117572566+quadratech188@users.noreply.github.com)
- Create README (117572566+quadratech188@users.noreply.github.com)

* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com>
- Make Release field use tito's release var (quadratech188@gmail.com)
- Embed xdgpp statically (quadratech188@gmail.com)
- Update README.md (117572566+quadratech188@users.noreply.github.com)
- Create README (117572566+quadratech188@users.noreply.github.com)

* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-1
- new package built with tito

%autochangelog

