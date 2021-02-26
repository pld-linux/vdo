Summary:	Management tools for Virtual Data Optimizer
Summary(pl.UTF-8):	Narzędzia do zarządzania podsystemem Virtual Data Optimizer
Name:		vdo
Version:	6.2.3.91
Release:	2
License:	GPL v2
Group:		Applications/System
#Source0Download: https://github.com/dm-vdo/vdo/releases
Source0:	https://github.com/dm-vdo/vdo/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a4eeab4f23938683ef3c0d0bcd2e34ad
Patch0:		%{name}-x86.patch
Patch1:		%{name}-types.patch
URL:		http://github.com/dm-vdo/vdo
BuildRequires:	device-mapper-devel
BuildRequires:	libblkid-devel
BuildRequires:	libuuid-devel >= 2.23
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	valgrind
BuildRequires:	zlib-devel
Requires:	libuuid >= 2.23
Requires:	lvm2
Requires:	python3 >= 1:3.6
Requires:	python3-PyYAML >= 3.10
#Suggests:	kernel-kvdo >= 6.2
ExclusiveArch:	%{ix86} %{x8664} x32 aarch64 ppc ppc64 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the user-space management tools for VDO.

%description -l pl.UTF-8
Virtual Data Optimizer (VDO) to cel device mappera zapewniający
deduplikację, kompresję i "thin provisioning" na poziomie bloków.

Ten pakiet zawiera narzędzia przestrzeni użytkownika do zarządzania
VDO.

%package -n bash-completion-vdo
Summary:	Bash completion for VDO management commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów poleceń do zarządzania VDO
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-vdo
Bash completion for VDO management commands.

%description -n bash-completion-vdo -l pl.UTF-8
Bashowe uzupełnianie parametrów poleceń do zarządzania VDO.

%package support
Summary:	Support tools for Virtual Data Optimizer
Summary(pl.UTF-8):	Narzędzia wspomagające dla podsystemu Virtual Data Optimizer
Group:		Applications/System
Requires:	libuuid >= 2.23

%description support
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the user-space support tools for VDO.

%description support -l pl.UTF-8
Virtual Data Optimizer (VDO) to cel device mappera zapewniający
deduplikację, kompresję i "thin provisioning" na poziomie bloków.

Ten pakiet zawiera narzędzia wspomagające przestrzeni użytkownika dla
VDO.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPT_FLAGS="%{rpmcflags} -fno-omit-frame-pointer"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALLOWNER= \
	bindir=%{_bindir} \
	defaultdocdir=%{_docdir} \
	python3_sitelib=%{py3_sitescriptdir} \
	mandir=%{_mandir} \
	unitdir=%{systemdunitdir} \
	sysconfdir=%{_sysconfdir}

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post vdo.service

%preun
%systemd_preun vdo.service

%postun
%systemd_postun_with_restart vdo.service

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt README.md examples/{ansible,monitor}
%attr(755,root,root) %{_bindir}/vdo
%attr(755,root,root) %{_bindir}/vdo-by-dev
%attr(755,root,root) %{_bindir}/vdostats
%attr(755,root,root) %{_bindir}/vdodmeventd
%attr(755,root,root) %{_bindir}/vdodumpconfig
%attr(755,root,root) %{_bindir}/vdoforcerebuild
%attr(755,root,root) %{_bindir}/vdoformat
%attr(755,root,root) %{_bindir}/vdosetuuid
%{py3_sitescriptdir}/%{name}
%{systemdunitdir}/vdo.service
%{systemdunitdir}/vdo-start-by-dev@.service
/lib/systemd/system-preset/97-vdo.preset
%{_sysconfdir}/udev/rules.d/69-vdo-start-by-dev.rules
%{_mandir}/man8/vdo.8*
%{_mandir}/man8/vdostats.8*
%{_mandir}/man8/vdodmeventd.8*
%{_mandir}/man8/vdodumpconfig.8*
%{_mandir}/man8/vdoforcerebuild.8*
%{_mandir}/man8/vdoformat.8*
%{_mandir}/man8/vdosetuuid.8*

%files -n bash-completion-vdo
%defattr(644,root,root,755)
/etc/bash_completion.d/vdo
/etc/bash_completion.d/vdostats

%files support
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vdoaudit
%attr(755,root,root) %{_bindir}/vdodebugmetadata
%attr(755,root,root) %{_bindir}/vdodumpblockmap
%attr(755,root,root) %{_bindir}/vdodumpmetadata
%attr(755,root,root) %{_bindir}/vdolistmetadata
%attr(755,root,root) %{_bindir}/vdoreadonly
%attr(755,root,root) %{_bindir}/vdoregenerategeometry
%{_mandir}/man8/vdoaudit.8*
%{_mandir}/man8/vdodebugmetadata.8*
%{_mandir}/man8/vdodumpblockmap.8*
%{_mandir}/man8/vdodumpmetadata.8*
%{_mandir}/man8/vdolistmetadata.8*
%{_mandir}/man8/vdoreadonly.8*
%{_mandir}/man8/vdoregenerategeometry.8*
