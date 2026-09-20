# Pixel Partitioner Early-Userspace ADB Daemon

## Overview

`adbd.pixel_partitioner` is TreeForge's ARM64 device-side ADB daemon
for Pixel Partitioner and minimal early-userspace bring-up environments.

It is derived from Android 15 AOSP `packages/modules/adb`.

It preserves the standard ADB wire protocol and standard FunctionFS USB
transport while removing startup assumptions that require the Android
framework, Android property service, second-stage Android init, `/data`,
or Android SELinux domain transitions.

This profile is independent from TreeForge Recovery ADB.

## Build Identity

- Module: `adbd.pixel_partitioner`
- Binary: `pixel-partitioner-adbd`
- Architecture: ARM64
- Baseline: `android-15.0.0_r36`
- Source project: `platform/packages/modules/adb`
- Source revision: `a877adddefdf011bfb5d4045919c6df3d3727ed3`
- Product: `module_arm64-trunk_staging-eng`
- Compile profile: `PIXEL_PARTITIONER_EARLY_USERSPACE=1`

## Purpose

The daemon provides early root ADB access during Pixel Partitioner bring-up.

It is intended to work before a complete Pixel Partitioner userspace exists and
without depending on Android's runtime lifecycle.

## Protocol Compatibility

TreeForge does not intentionally modify the ADB wire protocol.

Inherited AOSP functionality includes:

- CNXN negotiation
- ADB packet framing
- transport handling
- shell protocol
- sync/file-transfer protocol
- FunctionFS transport
- ordinary host ADB compatibility

The normal ADB connection state remains `device`.

## Device Identity

The early-userspace profile does not read Android `ro.product.*`
properties for connection identity.

It advertises:

- `ro.product.name=treeforge`
- `ro.product.model=Pixel Partitioner`
- `ro.product.device=treeforge`

Shell hostname fallback:

`pixel-partitioner`

## Privilege Model

The daemon deliberately remains root.

It does not use Android properties to determine root state.

It does not depend on:

- `ro.secure`
- `ro.debuggable`
- `service.adb.root`

It does not drop to `AID_SHELL`.

It does not perform the normal Android minijail UID/GID privilege drop.

Expected daemon identity:

- UID 0
- GID 0

This is an early bring-up policy and is not intended to silently become a
production security policy.

## Authentication

Initial Pixel Partitioner bring-up uses:

`auth_required = false`

Android's `adbd_auth` framework context is not initialized.

The framework key notification normally performed after ADB TLS setup is
suppressed because no Android auth framework exists.

The normal ADB protocol and TLS implementation itself remain inherited
from AOSP.

### Security Warning

Physical USB access currently provides unauthenticated root ADB access.

This is intentional for bring-up.

A future TreeForge authentication/key-store policy can replace this policy
without changing the ADB wire protocol.

## USB FunctionFS

Supported transport:

- USB FunctionFS

Expected mount:

`/dev/usb-ffs/adb`

TreeForge retains AOSP's FunctionFS descriptors and endpoint handling.

The daemon does not own:

- configfs gadget creation
- gadget composition
- UDC selection
- UDC binding
- UDC unbinding
- USB kernel module loading

Those belong to Pixel Partitioner PID1.

## Android USB Properties

The Pixel Partitioner profile does not depend on:

- `sys.usb.adb.disabled`
- `sys.usb.ffs.ready`

TreeForge PID1 must observe FunctionFS readiness directly.

## Network ADB

Automatic TCP and VSOCK listeners are disabled for this initial profile.

The daemon does not use the Android startup properties:

- `service.adb.listen_addrs`
- `service.adb.tcp.port`
- `persist.adb.tcp.port`

If USB FunctionFS is unavailable, the daemon does not silently open a
network listener.

## Shell

The normal ADB shell protocol remains enabled.

The expected shell path remains the Bionic `_PATH_BSHELL`, normally:

`/system/bin/sh`

The Pixel Partitioner initramfs will provide:

`/system/bin/sh -> /bin/sh`

The initial `/bin/sh` provider is expected to be TreeForge's separate
BusyBox-based bring-up shell.

## Shell Environment

The Pixel Partitioner profile supplies:

- `HOME=/`
- `HOSTNAME=pixel-partitioner`
- `LOGNAME=root`
- `USER=root`
- `SHELL=/system/bin/sh`
- `TMPDIR=/tmp`
- `PATH=/bin:/sbin:/usr/bin:/usr/sbin:/system/bin`

It does not require `/data/local/tmp` to start an interactive shell.

## SELinux

Pixel Partitioner early userspace does not require Android's Recovery
`adbd -> shell` SELinux transition.

The profile skips the Android shell-domain transition.

The binary may still dynamically depend on `libselinux.so` because
inherited AOSP code contains SELinux-aware functionality.

A library dependency does not mean Android SELinux initialization is
required for the supported Pixel Partitioner startup path.

## Android Property Service

The supported startup path is designed not to require Android's property
service.

Property-dependent behavior bypassed by this profile includes:

- root privilege policy
- verified-boot authentication policy
- `ro.adb.secure`
- product CNXN identity
- shell hostname fallback
- TCP listener configuration
- USB-disabled monitoring
- FunctionFS-ready notification
- Android watchdog initialization
- Android ADB trace-property initialization

Some inherited Android-specific services may still reference Android
properties if explicitly invoked.

Those services are not considered supported Pixel Partitioner features unless
they are separately adapted and validated.

## `/data`

`/data` is not required for daemon startup.

Interactive shell uses:

`TMPDIR=/tmp`

Some inherited Android-specific commands may still contain `/data` paths.
Those commands are outside the initial supported contract.

## JDWP

JDWP initialization is disabled.

Android application/framework debugging is outside the scope of the
early-userspace daemon.

## mDNS

mDNS and Android wireless-debugging discovery are not supported by the
initial Pixel Partitioner profile.

Initial transport scope is USB FunctionFS.

## Watchdog

Android ADB watchdog initialization is disabled.

Transport online/offline callbacks do not update the Android watchdog
active-connection counter in Pixel Partitioner mode.

## File Transfer

The standard ADB sync protocol and file-transfer engine remain present.

Intended capabilities:

- `adb push`
- `adb pull`

For the Pixel Partitioner early-userspace profile, sync bypasses Android-specific
filesystem policy:

- Android `adbd_fs_config()` ownership/mode policy is not applied.
- Android filesystem capability-xattr policy is not applied.
- Android `selinux_android_restorecon()` is not invoked.
- Android device API-level state is not required for sync policy.

The normal AOSP sync file operations remain intact, including:

- file creation
- file reads and writes
- directory creation
- symlink handling
- mode handling
- timestamps

Files therefore follow the early-userspace filesystem's normal ownership
and permission behavior rather than Android platform filesystem
configuration tables.

`adb push` and `adb pull` remain device-validation pending until tested
with the Pixel Partitioner initramfs.

## Interactive Commands

Intended capability:

`adb shell`

Expected useful bring-up commands after the BusyBox shell provider exists
include:

- `uname`
- `dmesg`
- `mount`
- `ls`
- `cat`
- `ps`
- `grep`
- `hexdump`
- `mkdir`
- `cp`
- `dd`
- `sleep`

Available commands are determined by the shell provider rather than adbd.

## Android-Specific Features Not Initially Supported

The initial Pixel Partitioner contract does not include:

- Android package management
- APK installation
- Android framework services
- JDWP application debugging
- Android `adb root` property lifecycle
- Android `adb unroot` property lifecycle
- Android `adb tcpip` property lifecycle
- Android `adb usb` property lifecycle
- Android wireless debugging
- Android mDNS pairing
- Android framework reboot/property integration

Inherited source code may still contain implementations for some of these
features. Presence in source does not mean TreeForge supports them in the
Pixel Partitioner runtime.

## Runtime Requirements

Required:

- Linux kernel
- USB gadget support
- FunctionFS
- `/dev/usb-ffs/adb`
- Bionic dynamic linker
- complete ELF runtime dependency closure
- `/tmp`
- `/system/bin/sh` for shell access

## Expected Initramfs Layout

Expected initial layout:

    /system/bin/pixel-partitioner-adbd
    /system/bin/linker64
    /system/bin/sh -> /bin/sh
    /system/lib64/...
    /bin/sh
    /tmp
    /dev/usb-ffs/adb

The exact library set is determined from the built ELF dependency closure.

## Gadget Lifecycle

Expected TreeForge PID1 sequence:

    load required kernel modules
    mount configfs
    create USB gadget
    create ffs.adb function
    mount FunctionFS at /dev/usb-ffs/adb
    launch pixel-partitioner-adbd
    wait for FunctionFS descriptors
    link ffs.adb into gadget configuration
    select GS201 UDC
    bind UDC
    host ADB becomes available

## Capability Status

| Capability | Status |
| --- | --- |
| Standard ADB protocol | IMPLEMENTED / inherited |
| ARM64 daemon | BUILD VALIDATED |
| USB FunctionFS | IMPLEMENTED / device validation pending |
| Root daemon | IMPLEMENTED |
| Property-free startup | IMPLEMENTED |
| Android auth framework independence | IMPLEMENTED |
| Authentication | DISABLED intentionally |
| ADB TLS implementation | RETAINED |
| Android SELinux shell transition | DISABLED |
| `/data` required for startup | NO |
| `/tmp` shell temp directory | IMPLEMENTED |
| `adb shell` | DEVICE VALIDATION PENDING |
| `adb push` | DEVICE VALIDATION PENDING |
| `adb pull` | DEVICE VALIDATION PENDING |
| TCP ADB | UNSUPPORTED initially |
| VSOCK ADB | UNSUPPORTED initially |
| mDNS | UNSUPPORTED initially |
| JDWP | UNSUPPORTED initially |
| Android framework | NOT REQUIRED |
| Android property service | NOT REQUIRED by supported startup |
| configfs ownership | EXTERNAL: TreeForge PID1 |
| UDC ownership | EXTERNAL: TreeForge PID1 |

## Build Acceptance

Required before packaging:

    [PASS] adbd.pixel_partitioner builds
    [PASS] output is AArch64 ELF
    [PASS] no missing DT_NEEDED dependencies
    [PASS] capability documentation exists
    [PASS] security policy documented
    [PASS] unsupported functionality documented

## Device Acceptance

Required before runtime validation:

    [PASS] FunctionFS descriptors appear
    [PASS] USB gadget enumerates
    [PASS] TreeForge host adb detects device
    [PASS] adb shell works
    [PASS] shell UID is 0
    [PASS] adb push works
    [PASS] adb pull works
    [PASS] no Android property service required
    [PASS] no Android framework required
    [PASS] no /data required

## Packaging

Do not publish the provider merely because compilation succeeds.

Packaging follows successful build and ELF closure validation.

Intended experimental provider identity:

`pixel-partitioner-adbd`

## Source Patch

TreeForge patch:

`tools/adb/patches/pixel-partitioner-early-userspace-adbd.patch`

The Pixel Partitioner profile must remain independent from:

`TREEFORGE_RECOVERY_STANDALONE`
