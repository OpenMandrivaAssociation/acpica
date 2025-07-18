%global optflags %{optflags} -Wno-error=unknown-warning-option

#define TAG R%(echo %{version}|cut -b5-6)_%(echo %{version}|cut -b7-8)_%(echo %{version}|cut -b3-4)
%define TAG R%(echo %{version}|cut -b1-4)_%(echo %{version}|cut -b5-6)_%(echo %{version}|cut -b7-8)

Summary:	A set of tools to display and debug your BIOS ACPI tables
Name:		acpica
Version:	20250404
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		https://acpica.org
Source0:	https://github.com/acpica/acpica/archive/refs/tags/%{TAG}.tar.gz
# Extra sources and patches are takes from OpenSUSE
Source1:	ec_access.c
Source2:	acpi_genl.tar.bz2
Source3:	acpi_validate
Source4:	wmidump.tar.bz2
# Workaround for https://github.com/westes/flex/issues/339
# Remove once build succeeds without it
Patch0:		acpica-20180313-flex-workaround.patch
Patch2:		wmidump_add_she_bang.patch

%rename 	iasl
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glibc-devel

%description
The included tools share the same code as it is used in the ACPI
implementation of the kernel. The code of the acpica project is exactly
the same as the ACPI parser and interpreter code of the kernel and the
code gets synced regularly from the acpica project into the kernel.
E.g. if you identify bugs in the kernel's ACPI implementation it might
be easier to debug them in userspace if possible. If the bug is part of
the acpica code, it has to be submitted to the acpica project to get
merged into the mainline kernel sources.

%prep
%setup -q -n acpica-%{TAG} -a 2 -a 4
%autopatch -p1

%build
%set_build_flags
sed -i -e 's/_CYGWIN/_LINUX/g' -e 's/-Werror//g' generate/unix/Makefile.config
cc %{SOURCE1} %{optflags} -o ec_access
%make_build CC=%{__cc} CFLAGS="%{optflags}" -C acpi_genl
%make_build CC=%{__cc} CFLAGS="%{optflags}" -C wmidump
%make_build CC=%{__cc} OPT_CFLAGS="%{optflags}" OPT_LDFLAGS="%{build_ldflags}"

%install
install -Dm 755 %{SOURCE4} %{buildroot}%{_bindir}/acpi_validate
install -Dm 755 ec_access %{buildroot}%{_sbindir}/ec_access

install -Dm 755 wmidump/wmidump %{buildroot}%{_bindir}/wmidump
install -Dm 755 wmidump/wmixtract.py %{buildroot}%{_bindir}/wmixtract

install -Dm 755 acpi_genl/acpi_genl %{buildroot}%{_sbindir}/acpi_genl

%make_install

%files
%{_bindir}/acpiexamples
%{_bindir}/acpiexec
%{_bindir}/acpixtract
%{_bindir}/acpisrc
%{_bindir}/wmidump
%{_bindir}/wmixtract
%{_bindir}/acpidump
%{_bindir}/acpibin
%{_bindir}/acpihelp
%{_bindir}/acpi_validate
%{_bindir}/iasl
%{_sbindir}/acpi_genl
%{_sbindir}/ec_access
