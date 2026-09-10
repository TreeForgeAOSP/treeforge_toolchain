# Binary payload policy

Provider: `aosp-fastboot`
Release: `android-15.0.0_r36-linux-x86_64`

Canonical payload:

    bin/fastboot

Accepted SHA-256:

    340c23293ee6f3fb60d689e8c2042d23ef969d511981c2df3c423973d6ff4898

The compiled payload is intentionally not copied into the ordinary
source/publication tree.

Published payloads will be generated from the pinned source and build
recipe and distributed as immutable GitHub Release assets.

TreeForge will download the exact provider release, verify its archive
identity, verify all internal payload identities, and cache it for use.
