Name: vicinae
Version: 0.16.11
Release:        %autorelease
Summary: A focused launcher for your desktop - native, fast, extensible

License: GPLv3
URL: https://github.com/vicinaehq/vicinae
Source0: https://github.com/vicinaehq/vicinae/releases/download/v%{version}/vicinae-linux-x86_64-v%{version}.tar.gz

BuildRequires: gcc
# Requires:

%description


%prep
%autosetup


%build
%configure
%make_build


%install
%make_install


%check


%files
%license
%doc


%changelog
%autochangelog

