# Binary payload policy

Provider: `aosp-adbd-recovery`
Release: `android-15.0.0_r36-arm64`

Canonical payload:

    rootfs/system/bin/adbd

Accepted SHA-256:

    555ecbd819c6410811934236b02bc1ead86ffc10b5a2d8811b221a2dfc3863e1

The compiled payload is intentionally not copied into the ordinary
source/publication tree.

Published payloads will be generated from the pinned source and build
recipe and distributed as immutable GitHub Release assets.

TreeForge will download the exact provider release, verify its archive
identity, verify all internal payload identities, and cache it for use.
