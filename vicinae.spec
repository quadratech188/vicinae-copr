%global forgeurl https://github.com/vicinaehq/vicinae

Name: vicinae
Version: 0.28.1
Release: %autorelease
Summary: A focused launcher for your desktop — native, fast, extensible 

%{forgemeta}
License: GPLv3
URL: %{forgeurl}
Source0: %{forgesource}

BuildRequires: cmake
BuildRequires: g++
BuildRequires: git
BuildRequires: mold
BuildRequires: ninja-build
BuildRequires: nodejs-npm
BuildRequires: yq

# CMakeLists.txt
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Qml)
BuildRequires: pkgconfig(openssl)
BuildRequires: cmake(glaze)

# src/server/CMakeLists.txt
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiPrivate)
BuildRequires: cmake(Qt6QuickDialogs2)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(Qt6ShaderTools)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(numen)
BuildRequires: cmake(KF6SyntaxHighlighting)
BuildRequires: cmake(LayerShellQt)
BuildRequires: pkgconfig(xcb-keysyms)

# cmake/Wayland.cmake
BuildRequires: pkgconfig(wayland-protocols)

# Unspecified
BuildRequires: cmake(Qt6Keychain)
BuildRequires: pkgconfig(libqalculate)

Requires: qt6qml(org.kde.layershell)
Recommends: nodejs(engine)

%description

Vicinae (pronounced "vee-CHEE-nay") is a high-performance, native command
palette for your desktop.

Out of the box, Vicinae can be your:

- app search
- clipboard history
- text expander (snippets)
- file search
- browser tab switcher
- emoji picker
- calculator
- window switcher
- font browser
- volume controller

When you need more, Vicinae can be extended in several ways:

- React/Typescript extensions, compatible with the Raycast ecosystem. In-app
  integration with the Vicinae store and the Raycast store.
- Script commands, also compatible with the Raycast feature of the same name,
  with special Vicinae additions.
- dmenu style menu creation, the linux minimalist way!

%prep
%forgeautosetup

%build

VICINAE_GIT_TAG=$(yq '.release.tag' < manifest.yaml)
VICINAE_GIT_COMMIT_HASH=$(yq '.release.short_rev' < manifest.yaml)

%cmake -G Ninja \
	-DVICINAE_PROVENANCE=copr \
	-DVICINAE_GIT_TAG=v%{version} \
	-DVICINAE_GIT_COMMIT_HASH=${VICINAE_GIT_COMMIT_HASH} \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_SHARED_LIBS=OFF \
	-DUSE_SYSTEM_CMARK_GFM=OFF \
	-DUSE_SYSTEM_LAYER_SHELL=ON \
	-DUSE_SYSTEM_KF6=ON \
	-DUSE_SYSTEM_GLAZE=ON \
	-DUSE_SYSTEM_QT_KEYCHAIN=ON \
	-DUSE_SYSTEM_NUMEN=ON
%cmake_build

%install
%cmake_install

%files
%{_bindir}/vicinae
%{_libexecdir}/vicinae/vicinae-browser-link
%{_libexecdir}/vicinae/vicinae-data-control-server
%{_libexecdir}/vicinae/vicinae-server
%{_libexecdir}/vicinae/vicinae-file-indexer

%caps(cap_dac_override+ep) %{_libexecdir}/vicinae/vicinae-input-server

%{_prefix}/lib/systemd/user/vicinae.service
%{_prefix}/lib/modules-load.d/vicinae.conf
%{_datadir}/applications/vicinae.desktop
%{_datadir}/applications/vicinae-url-handler.desktop
%{_datadir}/icons/hicolor/512x512/apps/vicinae.png
%{_datadir}/vicinae/themes/*

%changelog
%autochangelog
