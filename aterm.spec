Summary:	aterm - terminal emulator in an X Window System
Summary(pl.UTF-8):	aterm - emulator terminala dla X Window System
Summary(pt_BR.UTF-8):	Um emulador de vt102 colorido
Name:		aterm
Version:	1.0.0
Release:	2
License:	GPL
Vendor:		Sasha Vasko <sashav@sprintmail.com>
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/aterm/%{name}-%{version}.tar.bz2
# Source0-md5:	ceb64c62ae243a7fc3ddb0d6f9a19faa
Source1:	%{name}.desktop
Patch0:		%{name}-utempter.patch
Patch1:		%{name}-wtmp.patch
Patch2:		%{name}-etc_dir.patch
URL:		http://www.afterstep.org/aterm.php
BuildRequires:	autoconf
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	utempter-devel
BuildRequires:	xorg-lib-libXt-devel
Requires:	terminfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
aterm is a colour vt102 terminal emulator based on rxvt 2.4.8 with
Alfredo Kojima's additions of fast transparency, intended as an
xterm(1) replacement for users who do not require features such as
Tektronix 4014 emulation and toolkit-style configurability. As a
result, aterm uses much less swap space -- a significant advantage on
a machine serving many X sessions. It was created with AfterStep
Window Manger users in mind, but is not tied to any libraries, and can
be used anywhere.

%description -l pl.UTF-8
aterm jest kolorowym emulatorem terminala vt102, opartym na rxvt 2.4.8
z dodatkami Afredo Kojima do szybkiej emulacji przezroczystości. W
założeniu ma zastąpić program xterm(1) użytkownikom nie wymagającym
takich rzeczy jak emulacja terminala Tektronix 4014 oraz
"toolkit-style configurability". W efekcie aterm używa dużo mniej
pamięci swap -- co jest dużą zaletą w systemach obsługujących liczne
sesje Xów. Został stworzony z myślą o użytkownikach AfterStepa, ale
nie jest związany z żadnymi specyficznymi bibliotekami i może być
używany gdziekolwiek.

%description -l pt_BR.UTF-8
Aterm é um emulador de terminal vt102 baseado no rxvt 2.4.8, com a
adição de fundo transparente. Aterm é um substituto para o xterm, mais
leve.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd autoconf
%{__autoconf}
cp -f ./configure ..
cd ..
LDFLAGS="%{rpmldflags} -lutempter -L%{_libdir}"
export LDFLAGS

%configure \
	--enable-ttygid \
	--enable-wtmp \
	--enable-background-image \
	--with-term=rxvt \
	--with-png \
	--with-jpeg \
	--enable-transparency \
	--enable-fading \
	--enable-menubar \
	--enable-graphics \
	--enable-xgetdefault \
	--enable-next-scroll
#	--enable-utmp \

CFLAGS="%{rpmcflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

tar -cf docs.tar doc/etc doc/menu

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog doc/README* doc/FAQ docs.tar
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/aterm
%{_desktopdir}/aterm.desktop
