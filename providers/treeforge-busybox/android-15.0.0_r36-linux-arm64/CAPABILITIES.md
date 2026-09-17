# TreeForge BusyBox capabilities

## Runtime contract

- Architecture: ARM64 / AArch64
- ABI: Linux
- libc: musl
- Linking: fully static
- PT_INTERP: absent
- DT_NEEDED: zero
- Android/Bionic dependency: none
- Device-specific dependency: none

## Early-userspace shell

BusyBox provides `ash`, with `sh` configured to use `ash`.

Important bring-up applets enabled include:

- ls, cat, cp, mv, rm, ln
- mkdir, mknod, chmod, chown
- mount, umount
- dmesg, ps
- kill, killall
- grep, sed, awk, cut
- head, tail, hexdump
- dd, sync
- sleep, usleep
- uname, hostname
- readlink, realpath
- find, xargs
- env, which
- date, touch
- insmod, rmmod, modprobe, lsmod
- switch_root
- devmem
- watch, timeout
- strings, stat
- sha256sum

Consumers are responsible for creating the desired BusyBox applet symlinks.
For the ChromiumOS early-userspace ADB consumer this includes, at minimum:

    /bin/sh -> busybox
    /system/bin/sh -> /bin/sh

## Security model

BusyBox itself does not provide authentication or privilege separation.
Applet privileges are those of the process invoking BusyBox.

## Source availability

The provider release carries the corresponding BusyBox 1.36.1 source archive,
the exact build configuration, GPL-2.0 license material, and build provenance.
