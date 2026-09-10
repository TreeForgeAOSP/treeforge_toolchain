# Binary payload policy

Provider: `aosp-fastbootd`
Release: `android-15.0.0_r36-arm64`

Canonical payload:

    rootfs/system/bin/fastbootd

Accepted SHA-256:

    36079d453dda5f10a23dcf7f09b5dcb886f59fe983f12b658a1c0830c2f75bec

The compiled payload is intentionally not copied into the ordinary
source/publication tree.

Published payloads will be generated from the pinned source and build
recipe and distributed as immutable GitHub Release assets.

TreeForge will download the exact provider release, verify its archive
identity, verify all internal payload identities, and cache it for use.
