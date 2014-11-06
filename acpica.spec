Summary:	A set of tools to display and debug your BIOS ACPI tables
Name:		acpica
Version:	20140926
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://acpica.org
# Sources and patches are takes from OpenSUSE
Source0:	https://acpica.org/sites/acpica/files/acpica-unix2-%{version}.tar.gz
Source1:	ec_access.c
Source2:	acpi_genl.tar.bz2
Source3:	acpi_validate
Source4:	wmidump.tar.bz2
Patch1:		acpica-no-compiletime.patch
Patch2:		wmidump_add_she_bang.patch
Patch3:         debian-big_endian.patch
Patch4:         debian-unaligned.patch
Patch5:         name-miscompare.patch

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
%setup -q -n acpica-unix2-%{version} -a 2 -a 4
%apply_patches

%build
cc %{SOURCE1} %{optflags} -o ec_access
%make -C acpi_genl CFLAGS="%{optflags}"
%make -C wmidump CFLAGS="%{optflags}"
%make OPT_CFLAGS="%{optflags}"

%install
install -Dm 755 %{SOURCE4} %{buildroot}%{_bindir}/acpi_validate
install -Dm 755 ec_access %{buildroot}%{_sbindir}/ec_access

install -Dm 755 wmidump/wmidump %{buildroot}%{_bindir}/wmidump
install -Dm 755 wmidump/wmixtract.py %{buildroot}%{_bindir}/wmixtract

install -Dm 755 acpi_genl/acpi_genl %{buildroot}%{_sbindir}/acpi_genl

%makeinstall_std

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
%{_bindir}/acpinames
%{_bindir}/acpi_validate
%{_bindir}/iasl
%{_sbindir}/acpi_genl
%{_sbindir}/ec_access

