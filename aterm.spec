Summary:	aterm - terminal emulator in an X Window System
Summary(pl):	aterm - emulator terminala dla X Window System
Name:		aterm
Version:	0.3.6
Release:	2
License:	GPL
Group:		X11/Utilities
Group(pl):	X11/Narzêdzia
Vendor:		Sasha Vasko <sashav@sprintmail.com>
URL:		http://members.xoom.com/sashav/aterm
Source0:	http://members.xoom.com/sashav/aterm/%{name}-%{version}.tar.gz
Source1:	aterm.desktop
Patch0:		aterm-utempter.patch
Patch1:		aterm-wtmp.patch
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_prefix	/usr/X11R6
%define		_mandir /usr/X11R6/man

%description
aterm is a colour vt102 terminal emulator based on rxvt 2.4.8 with Alfredo
Kojima's additions of fast transparency, intended as an xterm(1)
replacement for users who do not require features such as Tektronix 4014
emulation and toolkit-style configurability. As a result, aterm uses much
less swap space -- a significant advantage on a machine serving many X
sessions.  It was created with AfterStep Window Manger users in mind, but
is not tied to any libraries, and can be used anywhere.

%description -l pl
aterm jest kolorowym emulatorem terminala vt102, opartym na rxvt 2.4.8 z
dodatkami Afredo Kojima do szybkiej emulacji przezroczysto¶ci. W za³o¿eniu
ma zast±piæ program xterm(1) u¿ytkownikom nie wymagaj±cym takich rzeczy jak
emulacja terminala Tektronix 4014 oraz "toolkit-style configurability".
W efekcie aterm u¿ywa du¿o mniej pamiêci swap -- co jest du¿± zalet± w
systemach obs³uguj±cych liczne sesje Xów. Zosta³ stworzony z my¶l± o
u¿ytkownikach AfterStepa, ale nie jest zwi±zany z ¿adnymi specyficznymi
bibliotekami i mo¿e byæ u¿ywany gdziekolwiek.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-s -lutempter"; export LDFLAGS;
%configure \
	--enable-utmp \
	--enable-wtmp \
	--enable-background-image \
	--with-term="xterm-color" \
	--with-png \
	--with-jpeg \
	--enable-transparency \
	--enable-menubar \
	--enable-graphics \
	--enable-next-scroll \
	--enable-xgetdefault

CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/share/applnk/Utilities

make DESTDIR=$RPM_BUILD_ROOT install
install %{SOURCE1} $RPM_BUILD_ROOT%{_prefix}/share/applnk/Utilities

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/aterm.1 ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc ChangeLog.gz
%attr(755,root,root) %{_bindir}/aterm
%{_mandir}/man1/aterm.1.gz
%{_prefix}/share/applnk/Utilities/aterm.desktop
