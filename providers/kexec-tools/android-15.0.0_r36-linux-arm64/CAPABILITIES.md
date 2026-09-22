# TreeForge kexec-tools capabilities

## Runtime contract

- Architecture: ARM64 / AArch64
- ABI: Linux
- libc: musl
- Linking: fully static
- PT_INTERP: absent
- DT_NEEDED: zero
- Android/Bionic dependency: none
- Device-specific dependency: none

## Function

This provider supplies the userspace `kexec` loader from kexec-tools
2.0.32 for early-userspace and recovery-style TreeForge runtimes.

The executable does not enable kexec in the kernel. Consumers require a
running kernel with the applicable kexec syscall support and are
responsible for supplying the kernel image, initramfs, device-tree data,
and command line required for the target boot.

## Build feature scope

The TreeForge runtime build intentionally disables:

- zlib
- liblzma
- libzstd
- Xen support

This keeps the provider self-contained and avoids adding compression
libraries to early userspace.

## Source availability

The release carries the exact kexec-tools 2.0.32 source archive,
upstream license material, generated configure state, and build
provenance.
