%define name aterm
%define version 0.3.6
%define release 1
%define serial 1

Summary: aterm - terminal emulator in an X window
Name: %{name}
Version: %{version}
Release:%{release}
Epoch: %{serial}
Copyright: GPL
Group: X11/Utilities
Vendor: Sasha Vasko <sashav@sprintmail.com>
URL: http://members.xoom.com/sashav/aterm
Distribution: Freshmeat RPMs
Packager: Ryan Weaver <ryanw@infohwy.com>
Source: http://members.xoom.com/sashav/aterm/%{name}-%{version}.tar.gz
Source1: aterm.wmconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
aterm, version %{version}, is a colour vt102 terminal emulator based on
rxvt 2.4.8 with Alfredo Kojima's additions of fast transparency,
intended as an xterm(1) replacement for users who do not require
features such as Tektronix 4014 emulation and toolkit-style
configurability. As a result, aterm uses much less swap space -- a
significant advantage on a machine serving many X sessions.

It was created with AfterStep Window Manger users in mind, but is not
tied to any libraries, and can be used anywhere.

%prep
%setup -q

CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=/usr/X11R6 \
	--enable-utmp \
	--enable-wtmp \
	--enable-background-image \
	--with-png \
	--with-jpeg \
	--enable-transparency \
	--enable-menubar \
	--enable-graphics \
	--enable-next-scroll \
	--disable-backspace-key \
	--disable-delete-key \
	--enable-xgetdefault

%build
make

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT/usr/X11R6
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig

make prefix=$RPM_BUILD_ROOT/usr/X11R6 install
install -m 644 $RPM_SOURCE_DIR/aterm.wmconfig $RPM_BUILD_ROOT/etc/X11/wmconfig/aterm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc ChangeLog
/usr/X11R6/bin/aterm
/usr/X11R6/man/man1/aterm.1
%config(missingok) /etc/X11/wmconfig/aterm

%changelog
* Fri Feb 26 1999 Ryan Weaver <ryanw@infohwy.com>
  [aterm-0.3.4-1]

- main.c: (SetBackgroundType()) - now correctly checks for shading being 100
  and allows for fast transparency/tinting in that case. That brings fast 
  transparency back in bussiness.
- main.c: (resize_windows()) - now checks if root background has changed, and
  updates window even if it was not moved in this case. 
- main.c: (resize_windows()) - removed strange event checking loop so to get 
  rid of unresized window problem, when resizing very fast.
- screen.c: (CLEAR_CHARS(),CLEAR_ROWS()) - hopefully fixed random occuring bug
  when parts of the window close to the border were not cleared sometimes.
- main.c: (resize_windows()) - fixed bug when window contents gets flushed on
  window move, if compiled without transparency and background image. 
- command.c: (process_x_event()) ReparentNotify message handler fixed to
  set parent windows backgrounds to ParentRelative in any transparency mode -
  that should fix problems that KDE users were having with it. 
  Also XErrorHandler is set here to prevent crashes on Window Manager restarts.
- ximage_utils.c: (ShadeXImage()) moved here from pixmap.c
- ximage_utils.c: added some ifdefs to enable easy porting to/from AfterStep
- ximage_utils.c: (ShadeXImage()) - uses correct data types for pointers - as
  the result shading should work fine now on 64-bit CPUs
- pixmap.c: (GetMyPosition()) split in two - GetWinPosition() - more generic
  function.
- pixmap.c: (GetMyPosition()) now sets error handler to prevent crashes - when
  restarting window manager.
- pixmap.c: (ValidateSrcPixmap()) split in two ValidatePixmap() - is more 
  generic version. ValidateSrcPixmap() is resetting root background ID if it 
  changed.
- pixmap.c: (CutPixmap()) chaged to more generic CutWinPixmap().
- pixmap.c: changed to reflect all this changes above.
- configure.in: minor changes to improve libasimage detection.   
- rxvt.h: SB_WIDTH and other scrollbar parameters has been moved to feature.h
  so ppl don't have to edit rxvt.h every time they upgrade.

* Mon Feb 22 1999 Ryan Weaver <ryanw@infohwy.com>
  [aterm-0.3.3-1]
- Added -sh %, -bgtype <type>, -txttype <type>, -tinttype <type> options.
- Changed -tint to -tint <color> to make possible different background and 
  tinting colors.
- Changed -pixmap <file[;geom]> meaning of geom now is the area of original 
  image, to be cut out, and used as the background. 
- src/pixmap.c: complete rewrite of everything that was in there, to enable
  all those cool transformations. Includes Shading functions, stretching/
  scaling/etc function, capturing of the root background, if root pixmap ID is
  not available.X errors handling to prevent crashing.
- Added ximage_utils.c from AfterStep's libasimage, to be used when libasimage
  cannot be found, or linked with.
- rxvt.h: Added ShadingInfo and BackgroundInfo structures to hold all 
  background image information. Respectively TermWin.background  member was 
  added
- rxvt.h: added one more color definition : tintColor
- rxvt.h: added variables to hold all those new options.
- main.c: added Background information initialization functions, and textType,
  tintType, and bgType parsing functions.
- main.c: (CreateWindows())tintGC only created if we do fast transparency.
- main.c: (CreateWindows())text GC is created using txttype option's function.
- main.c: (resize_window())completely reworked to accomodate all new 
  capabilities. It now checks for visibility, changed absolute position and 
  size of the window prior to do any tinting/shading/rendering. That sometimes
  causing aterm not to perform shading on startup - will fix later.
- main.c: (resize_window1())does not do scr_clear() anymore - it's done 
  outside of it if needed.
- command.c: PropertyChanged event handler modifyed to check for visibility
  prior to do tinting/shading/rendering.
- screen.c: fast tinting is performed only if tintGC is available, instead
  of checking for Opt_tint.
- command.c: added Rafal Wierzbicki changes to support for Unix98 ptys with 
  linux-2.2.x and glibc-2.1
- added tools dir, and tools/makeatermversion script to automate new aterm 
  version creating/tar-balling.
- man pages hopefully updated. 

* Sat Jan 16 1999 Ryan Weaver <ryanw@infohwy.com>
  [aterm-0.3.2-1]
- src/rxvt.h ParentWin1, ParentWin2 changed to array, first elem of which 
  should always be main window of aterm (TermWin.parent)
- src/main.c (resize_window()) added check for event code, not only event 
  type, when checking for queued resizing events.
  That allows filtering of events that has nothing to do with resizing,
  and fixes screen refresh problems when aterm is mapped/unmapped.
- src/screen.c (scr_clear_tint()) removed ClearWindow for parent windows.
  That seems to be unneccessary and that was causing aterm death on 
  window manager restart.
- src/main.c (resize_window()) changed to not query size of toppest parent 
  window as far as it can become invalid on window manager's restart. 
  That was also causing aterm's death on Window Manager restarts.

* Thu Jan 14 1999 Ryan Weaver <ryanw@infohwy.com>
  [aterm-0.3.1-1]
- src/command.c (process_x_event()) added check for _XROOTPMAP_ID value -
  so not to refresh screen when it's None - that fixes problem with aterm
  dieing on AfterStep restart.


* Thu Jan 14 1999 Ryan Weaver <ryanw@infohwy.com>
  [aterm-0.3.0-1]
- started new development version. USE IT WITH CAUTION !!!
- Changed --enable-background-xpm to --enable-background-image. Due to wider
  image format support it makes better sense.
- Added optional integration with AfterStep libraries for wider image format
  support. JPEG and PNG images can now be used as background, 
  if shared AfterStep libraries are installed on system.
  libJPEG v.6.0a and/or libPNG v.1.0.2 or greater required.
  Imaging library detection macros has been taken from AfterStep distribution.
  AfterStep libs will only be used if configured with --enable-background-image
  flag.
- --enable-aftersteplibs configure flag added to enable/disable AfterStep
  integration. Enabled by default. 
- the following configure options added to enable/disable image library usage :
  --with-xpm-includes=DIR use XPM includes in DIR
  --with-xpm-library=DIR  use XPM library in DIR
  --with-xpm              use XPM
  --with-jpeg-includes=DIR use JPEG includes in DIR
  --with-jpeg-library=DIR  use JPEG library in DIR
  --with-jpeg              support JPEG image format [yes]
  --with-png-includes=DIR use PNG includes in DIR
  --with-png-library=DIR  use PNG library in DIR
  --with-png              support PNG image format [yes]
- src/feature.h removed obsolete code for XPM_BUFFERING support.
- src/main.c (resize_window()) fixed bug when transparent background gets 
  garbled, when Shading/Unshading aterm in AfterStep.
- src/screen.c scr_clear() changed into scr_clear_tint(int bWithTinting) 
  to enable/disable tinting while clearing window. scr_clear() is now
  a macro calling scr_clear_tint(1).
- src/screen.c (scr_clear_tint()) fixed minor bug in tinting code
  to use TermWin_internalBorder instead of BORDERWIDTH
- src/screen.c (CLEAR_CHARS(),CLEAR_ROWS()) fixed bug when clearing
  screen will keep tine border around window untinted.
  ( based on contribution from Michael Bruun Petersen" <mbp@image.dk>)
- src/main.c added (SetBackgroundPixmap(char* PixmapSpec)) to parse pixmap
  specification load/scale pixmap.
- src/main.c (change_font()) added sanity check for font width, that will
  hopefully prevent aterm from crashing, when using some fonts.
  ( thanks to <suchness> for suggestion ).
- src/xpm.c moved to src/pixmap.c due to wider image format support that
  makes better sense.
- src/pixmap.c removed obsolete code for XPM_BUFFERING
- src/pixmap.c (set_bgPixmap()) modifyed for optional utilization of 
  AfterStep libraries.
- src/pixmap.c (resize_pixmap()) added support to prevent pixmap from 
  tiling vertical, horizontal or in both directions. See src/feature.h
  to enable/disable this.
  ( contributed by Eric Tremblay <deltax@dsuper.net> )
- src/rxvt.h   added :
  #include <sys/int_types.h> 
  to fix compilation problems on some Solaris boxes.
  ( suggested by Albert Dorofeev <tigr@tigr.net> )
- src/scrollbar2.c rewrote NeXT scrollbar code for better portability
  and configurability. Now scrollbar width and look can be changed at 
  compile time, using options in rxvt.h.
- src/rxvt.h added bunch of defines to enable NeXT scrollbar tweaking at 
  compile time:
    /* could be anything from 13 to 19  but the true NeXT is 17 */ 
    # define SB_WIDTH		17 
    /* this will define somemore parameters for shaping NeXTish scrollbars */
    /* NEXT_SCROLL_CLEAN if defined removes shades of gray from buttons */
    # undef NEXT_SCROLL_CLEAN   
    # define NEXT_SCROLL_SQUARE_ARROWS 
    # define SB_BORDER_WIDTH 1
    /* this makes buttons thinner then scrollbar's base ( if more then 0 ) */ 
    # define SIDE_STEP_WIDTH 0
    /* end NeXT scrollbar specific fetures */

* Thu Dec 31 1998 Ryan Weaver <ryanw@infohwy.com>
  [aterm-0.2.0-1]
- First RPM
- *Converted documentation to aterm vs. rxvt
- *src/features.h [ATERM_PATH_ENV]: Added ATERMPATH env. variable to
  define PATH where to search for files. Aterm is now looking in ATERMPATH,
  then RXVTPATH, and only then in PATH.
- * --enable-transparency and --enable-next-scroll are now set by default.
