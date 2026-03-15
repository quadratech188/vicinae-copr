Name: vicinae
Version: 0.20.6
Release: 2%{?dist}
Summary: A focused launcher for your desktop — native, fast, extensible 

License: GPLv3
URL: https://github.com/vicinaehq/vicinae
Source0: https://github.com/vicinaehq/vicinae/archive/refs/tags/v%{version}.tar.gz
Patch0: 0001-fix-Include-unistd-explicitly.patch

# https://docs.vicinae.com/build#build-requirements
BuildRequires: git
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
BuildRequires: libicu-devel
BuildRequires: kf6-syntax-highlighting-devel

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
%autosetup -p1


%build

VICINAE_GIT_TAG=$(yq '.release.tag' < manifest.yaml)
VICINAE_GIT_COMMIT_HASH=$(yq '.release.short_rev' < manifest.yaml)

%cmake -G Ninja \
	-DVICINAE_PROVENANCE=copr \
	-DVICINAE_GIT_TAG=v%{version} \
	-DVICINAE_GIT_COMMIT_HASH=${VICINAE_GIT_COMMIT_HASH} \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_SHARED_LIBS=OFF \
%cmake_build

%install
%cmake_install

%files
%{_bindir}/vicinae
%{_libexecdir}/vicinae/vicinae-browser-link
%{_libexecdir}/vicinae/vicinae-data-control-server
%{_libexecdir}/vicinae/vicinae-server
%{_libexecdir}/vicinae/vicinae-snippet-server

%{_prefix}/lib/systemd/user/vicinae.service
%{_prefix}/lib/udev/rules.d/70-vicinae.rules
%{_prefix}/lib/modules-load.d/vicinae.conf
%{_datadir}/applications/vicinae.desktop
%{_datadir}/applications/vicinae-url-handler.desktop
%{_datadir}/icons/hicolor/512x512/apps/vicinae.png
%{_datadir}/vicinae/themes/*

%{_datadir}/vicinae/native-messaging-hosts/com.vicinae.vicinae.chromium.json.in
%{_datadir}/vicinae/native-messaging-hosts/com.vicinae.vicinae.firefox.json.in
/etc/chromium/native-messaging-hosts/com.vicinae.vicinae.json
/usr/lib/mozilla/native-messaging-hosts/com.vicinae.vicinae.json

%license LICENSE

%changelog
* Sun Mar 15 2026 Quadratech188 <quadratech188@gmail.com> 0.20.6-2
- fix: Include unistd explicity (quadratech188@gmail.com)

* Sun Mar 15 2026 quadratech188 <quadratech188@gmail.com> 0.20.6-1
- chore: Bump to v0.20.6 (quadratech188@gmail.com)

* Tue Mar 10 2026 quadratech188 <quadratech188@gmail.com> 0.20.5-1
- chore: Bump to v0.20.5 (quadratech188@gmail.com)
- fix: Check exit codes (quadratech188@gmail.com)
- build: Rewrite update script (quadratech188@gmail.com)

* Mon Mar 09 2026 Quadratech188 <quadratech188@gmail.com> 0.20.4-2
- refactor: Remove old workaround (quadratech188@gmail.com)
* Mon Mar 09 2026 quadratech188 <quadratech188@gmail.com> 0.20.4-1
- chore: Bump to v0.20.4 (quadratech188@gmail.com)

* Fri Mar 06 2026 Quadratech188 <quadratech188@gmail.com> 0.20.3-2
- fix: Add udev files (quadratech188@gmail.com)

* Fri Mar 06 2026 quadratech188 <quadratech188@gmail.com> 0.20.3-1
- chore: Bump to v0.20.3 (quadratech188@gmail.com)

* Sun Mar 01 2026 quadratech188 <quadratech188@gmail.com> 0.20.2-1
- chore: Bump to v0.20.2 (quadratech188@gmail.com)

* Sat Feb 28 2026 quadratech188 <quadratech188@gmail.com> 0.20.1-1
- chore: Bump to v0.20.1 (quadratech188@gmail.com)

* Fri Feb 27 2026 Quadratech188 <quadratech188@gmail.com> 0.20.0-2
- chore: Add kf6-syntax-highlighting-devel dependency (quadratech188@gmail.com)

* Fri Feb 27 2026 quadratech188 <quadratech188@gmail.com> 0.20.0-1
- chore: Bump to v0.20.0 (quadratech188@gmail.com)

* Tue Feb 17 2026 quadratech188 <quadratech188@gmail.com> 0.19.9-1
- chore: Bump to v0.19.9 (quadratech188@gmail.com)

* Sat Feb 14 2026 Quadratech188 <quadratech188@gmail.com> 0.19.8-2
- fix: Add native messaging host templates to package (quadratech188@gmail.com)

* Sat Feb 14 2026 quadratech188 <quadratech188@gmail.com> 0.19.8-1
- chore: Bump to v0.19.8 (quadratech188@gmail.com)

* Tue Feb 10 2026 quadratech188 <quadratech188@gmail.com> 0.19.7-1
- chore: Bump to v0.19.7 (quadratech188@gmail.com)

* Sat Feb 07 2026 quadratech188 <quadratech188@gmail.com> 0.19.6-1
- chore: Bump to v0.19.6 (quadratech188@gmail.com)
- fix: Add files for 0.19.4 (quadratech188@gmail.com)

* Fri Feb 06 2026 quadratech188 <quadratech188@gmail.com> 0.19.5-1
- chore: Bump to v0.19.5 (quadratech188@gmail.com)

* Fri Feb 06 2026 quadratech188 <quadratech188@gmail.com> 0.19.4-1
- chore: Bump to v0.19.4 (quadratech188@gmail.com)
- fix: Pull remote before updating (quadratech188@gmail.com)

* Mon Feb 02 2026 Quadratech188 <quadratech188@gmail.com> 0.19.3-1
- chore: Bump to v0.19.3 (quadratech188@gmail.com)

* Fri Jan 23 2026 Quadratech188 <quadratech188@gmail.com> 0.19.1-1
- chore: Bump to v0.19.1 (quadratech188@gmail.com)

* Wed Jan 21 2026 Quadratech188 <quadratech188@gmail.com> 0.19.0-3
- fix: Include native messaging host spec files (quadratech188@gmail.com)

* Tue Jan 20 2026 Quadratech188 <quadratech188@gmail.com> 0.19.0-2
- fix: Remove patch from spec file (quadratech188@gmail.com)

* Tue Jan 20 2026 Quadratech188 <quadratech188@gmail.com> 0.19.0-1
- chore: Bump to v0.19.0 (quadratech188@gmail.com)
- chore: Remove upstreamed patch (quadratech188@gmail.com)

* Fri Jan 09 2026 Quadratech188 <quadratech188@gmail.com> 0.18.3-1
- chore: Bump to v0.18.3 (quadratech188@gmail.com)

* Fri Jan 09 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-7
- fix: Final <range> header (quadratech188@gmail.com)

* Thu Jan 08 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-6
- fix: Add additional includes (quadratech188@gmail.com)

* Thu Jan 08 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-5
- fix: Repair changelog (quadratech188@gmail.com)

* Thu Jan 08 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-4
- fix: Additional <range> includes (quadratech188@gmail.com)

* Thu Jan 08 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-3
- fix: Fix patch (quadratech188@gmail.com)

* Thu Jan 08 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-2
- fix: Patch build failure due to relying on generated headers
  (quadratech188@gmail.com)

* Thu Jan 08 2026 Quadratech188 <quadratech188@gmail.com> 0.18.2-1
- chore: Bump to v0.18.2 (quadratech188@gmail.com)

* Tue Jan 06 2026 Quadratech188 <quadratech188@gmail.com> 0.18.1-2
- fix: Include libicu dev files in build (quadratech188@gmail.com)

* Mon Jan 05 2026 Quadratech188 <quadratech188@gmail.com> 0.18.1-1
- chore: Bump to v0.18.1 (quadratech188@gmail.com)

* Sun Jan 04 2026 Quadratech188 <quadratech188@gmail.com> 0.18.0-1
- chore: Bump to v0.18.0 (quadratech188@gmail.com)

* Fri Dec 26 2025 Quadratech188 <quadratech188@gmail.com> 0.17.3-1
- chore: Bump to v0.17.3 (quadratech188@gmail.com)

* Tue Dec 23 2025 Quadratech188 <quadratech188@gmail.com> 0.17.2-1
- chore: Bump to v0.17.2 (quadratech188@gmail.com)
- fix: glaze headers aren't installed in vicinae >= 0.17.2
  (quadratech188@gmail.com)

* Mon Dec 22 2025 Quadratech188 <quadratech188@gmail.com> 0.17.1-3
- fix: Ignore files installed by glaze (quadratech188@gmail.com)

* Mon Dec 22 2025 Quadratech188 <quadratech188@gmail.com> 0.17.1-2
- fix: Add git to dependencies to allow fetching glaze
  (quadratech188@gmail.com)

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
- PLACEHOLDER

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

* Thu Dec 04 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-5
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

* Wed Dec 03 2025 Quadratech188 <quadratech188@gmail.com> 0.16.11-1
- new package built with tito

%autochangelog

