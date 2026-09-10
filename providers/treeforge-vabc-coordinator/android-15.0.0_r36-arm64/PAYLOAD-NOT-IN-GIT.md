# Binary payload policy

Provider: `treeforge-vabc-coordinator`
Release: `android-15.0.0_r36-arm64`

Canonical payload:

    rootfs/system/bin/treeforge-vabc-coordinator

Accepted SHA-256:

    666417386eb6c0ba9d1c3e197b585879d3bc05cdb9ed4c9f1d40944ed969d393

The compiled payload is intentionally not copied into the ordinary
source/publication tree.

Published payloads will be generated from the pinned source and build
recipe and distributed as immutable GitHub Release assets.

TreeForge will download the exact provider release, verify its archive
identity, verify all internal payload identities, and cache it for use.
